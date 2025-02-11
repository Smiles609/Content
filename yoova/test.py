import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

# Request model for script generation
class ScriptRequest(BaseModel):
    topic: str
    style: Optional[str] = "informative"

# Response model for script generation
class ScriptResponse(BaseModel):
    script: str

# Request model for channel name generation
class ChannelNameRequest(BaseModel):
    topic: str
    keywords: Optional[str] = None

# Response model for channel name generation
class ChannelNameResponse(BaseModel):
    channel_name: str

# Request model for niche suggestion
class NicheSuggestionRequest(BaseModel):
    interests: str

# Response model for niche suggestion
class NicheSuggestionResponse(BaseModel):
    niche_suggestions: str


# Replace with your Google Gemini API URL and credentials
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"  # Updated to use gemini-1.5-flash
API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY") # Replace with your actual API key

def generate_script(topic: str, style: str) -> str:
    """
    Generates a script using the Google Gemini API.
    
    Args:
        topic (str): The topic of the script.
        style (str): The style of the script.

    Returns:
       str: The generated script, or error if it could not be generated.
    
    Raises:
        HTTPException: if the Google Gemini API returns an error.
    """
    # Prepare the payload to send to Google Gemini API
    payload = {
       "contents": [
        {
          "parts": [
             {
              "text": f"""
              You are an expert script writer who creates high quality video scripts.
               
              Generate a video script about '{topic}' in a '{style}' style. 
              """
              }
           ]
         }
       ]
    }

    headers = {
        "Content-Type": "application/json",
         "x-goog-api-key": f"{API_KEY}"
    }

    # Send a POST request to Google Gemini API
    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        # Extract script content from the response
        try:
          result = response.json()
          
          
          script = result["candidates"][0]["content"]["parts"][0]["text"]
          return script
        except (KeyError,IndexError):
          raise HTTPException(status_code=500, detail="Error processing the response from Gemini API")

    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error generating script with Gemini API: {response.text}")


def suggest_channel_name(topic: str, keywords: Optional[str] = None) -> str:
    """
    Suggests a unique channel name using the Google Gemini API.

    Args:
        topic (str): The topic of the channel.
        keywords (Optional[str]): Optional keywords to consider.

    Returns:
        str: A suggested channel name.

    Raises:
        HTTPException: If there is an error with the Gemini API.
    """
    prompt = f"Suggest a unique and catchy YouTube channel name about '{topic}'."
    if keywords:
        prompt += f" Include these keywords: {keywords}."
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": f"{API_KEY}"
    }
    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        try:
           result = response.json()
           channel_name = result["candidates"][0]["content"]["parts"][0]["text"]
           return channel_name
        except (KeyError, IndexError):
            raise HTTPException(status_code=500, detail="Error processing response from Gemini API")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error generating channel name with Gemini API: {response.text}")


def suggest_niche(interests: str) -> str:
    """
    Suggests a niche for a YouTube channel based on the provided interests using the Google Gemini API.

    Args:
        interests (str): The user's interests or areas they are considering.

    Returns:
       str: A JSON containing niche suggestions.

    Raises:
        HTTPException: if the Google Gemini API returns an error.
    """

    prompt = f"""
    You are an expert in identifying profitable and trending niches.
    
    Based on the following interests: {interests}, suggest several specific YouTube channel niches
    that could be successful, along with reasons why.
    """
    payload = {
      "contents": [
        {
          "parts": [
             {
                "text": prompt
             }
          ]
         }
       ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": f"{API_KEY}"
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        try:
          result = response.json()
          niche_suggestions = result["candidates"][0]["content"]["parts"][0]["text"]
          return niche_suggestions
        except (KeyError, IndexError):
           raise HTTPException(status_code=500, detail="Error processing response from Gemini API")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error generating niche suggestions with Gemini API: {response.text}")

# API endpoint to generate video scripts
@app.post("/generate-script", response_model=ScriptResponse)
def generate_video_script(request: ScriptRequest):
    """
    API endpoint that takes a topic and style then generates a video script.

    Args:
        request (ScriptRequest): Incoming request with a topic and style.

    Returns:
        ScriptResponse: JSON response with the script.

    Raises:
       HTTPException: if there is an error with the request.
    """

    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required.")
    
    # Call the Google Gemini API for script generation
    try:
      script = generate_script(request.topic, request.style)
    except HTTPException as e:
      raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return ScriptResponse(script=script)


# API endpoint to suggest a youtube channel name
@app.post("/suggest-channel-name", response_model=ChannelNameResponse)
def suggest_youtube_channel_name(request: ChannelNameRequest):
    """
    API endpoint to suggest a YouTube channel name based on a topic and optional keywords.

    Args:
        request (ChannelNameRequest): The request containing the topic and keywords.

    Returns:
        ChannelNameResponse: The suggested channel name.

    Raises:
        HTTPException: If the topic is not provided or there is an error with the Google Gemini API.
    """
    if not request.topic:
      raise HTTPException(status_code=400, detail="Topic is required.")

    try:
      channel_name = suggest_channel_name(request.topic, request.keywords)
    except HTTPException as e:
      raise e
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return ChannelNameResponse(channel_name=channel_name)

# API endpoint to suggest a youtube channel niche
@app.post("/suggest-niche", response_model=NicheSuggestionResponse)
def suggest_youtube_niche(request: NicheSuggestionRequest):
    """
    API endpoint that takes user interests and returns niche suggestions.

    Args:
      request (NicheSuggestionRequest): The incoming request containing the interests.

    Returns:
      NicheSuggestionResponse: The suggested niche for a YouTube channel.
    Raises:
      HTTPException: If the interests are not provided, or if an error occurs during the API call.
    """

    if not request.interests:
        raise HTTPException(status_code=400, detail="Interests are required.")
    try:
        niche_suggestions = suggest_niche(request.interests)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return NicheSuggestionResponse(niche_suggestions=niche_suggestions)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)