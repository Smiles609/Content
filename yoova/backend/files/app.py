import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# --- CORS Configuration ---
origins = [
    "http://127.0.0.1:8080",  # Allow requests from your frontend origin
    "http://localhost:8080", # Allow from localhost
    # Add other allowed origins here (if any)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# --- YouTube Related Models and Functions ---
class ScriptRequest(BaseModel):
    topic: str
    style: Optional[str] = "informative"

class ScriptResponse(BaseModel):
    script: str

class ChannelNameRequest(BaseModel):
    topic: str
    keywords: Optional[str] = None

class ChannelNameResponse(BaseModel):
    channel_name: str

class NicheSuggestionRequest(BaseModel):
    interests: str

class NicheSuggestionResponse(BaseModel):
    niche_suggestions: str

class VideoIdeaRequest(BaseModel):
    topic: str
    keywords: Optional[str] = None

class VideoIdeaResponse(BaseModel):
    video_ideas: str

class PostContentRequest(BaseModel):
    topic: str
    keywords: Optional[str] = None
    style: Optional[str] = "engaging"

class PostContentResponse(BaseModel):
    post_content: str
    
# --- X (Twitter) Related Models and Functions ---
class TweetRequest(BaseModel):
    topic: str
    keywords: Optional[str] = None
    style: Optional[str] = "engaging"

class TweetResponse(BaseModel):
    tweet: str

# --- Instagram Related Models and Functions ---
class InstagramPostRequest(BaseModel):
    topic: str
    keywords: Optional[str] = None
    style: Optional[str] = "engaging"

class InstagramPostResponse(BaseModel):
    post_content: str

class InstagramStoryRequest(BaseModel):
    topic: str
    keywords: Optional[str] = None
    style: Optional[str] = "engaging"

class InstagramStoryResponse(BaseModel):
    story_content: str

class InstagramChannelNameRequest(BaseModel):
    topic: str
    keywords: Optional[str] = None

class InstagramChannelNameResponse(BaseModel):
    channel_name: str

class InstagramVideoIdeaRequest(BaseModel):
    topic: str
    keywords: Optional[str] = None

class InstagramVideoIdeaResponse(BaseModel):
    video_ideas: str

class InstagramNicheSuggestionRequest(BaseModel):
    interests: str

class InstagramNicheSuggestionResponse(BaseModel):
    niche_suggestions: str

class InstagramReelIdeaRequest(BaseModel):
    topic: str
    keywords: Optional[str] = None

class InstagramReelIdeaResponse(BaseModel):
    reel_ideas: str

class InstagramVideoScriptRequest(BaseModel):
    topic: str
    style: Optional[str] = "informative"

class InstagramVideoScriptResponse(BaseModel):
    script: str

# --- Email Related Models and Functions ---
class EmailRequest(BaseModel):
    topic: str
    style: Optional[str] = "professional"
    keywords: Optional[str] = None

class EmailResponse(BaseModel):
    email_content: str

# --- API Configuration ---
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

# --- YouTube Related Functions ---
def generate_script(topic: str, style: str) -> str:
    """Generates a script using the Google Gemini API."""
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
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        try:
          result = response.json()
          script = result["candidates"][0]["content"]["parts"][0]["text"]
          return script
        except (KeyError,IndexError):
          raise HTTPException(status_code=500, detail="Error processing the response from Gemini API")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error generating script with Gemini API: {response.text}")

def suggest_channel_name(topic: str, keywords: Optional[str] = None) -> str:
    """Suggests a unique channel name using the Google Gemini API."""
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
    """Suggests a niche for a YouTube channel based on provided interests."""
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

def generate_video_ideas(topic: str, keywords: Optional[str] = None) -> str:
    """Generates video ideas using the Google Gemini API."""
    prompt = f"Suggest several creative and engaging video ideas about '{topic}'."
    if keywords:
        prompt += f" Consider these keywords: {keywords}."
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
          video_ideas = result["candidates"][0]["content"]["parts"][0]["text"]
          return video_ideas
       except (KeyError, IndexError):
            raise HTTPException(status_code=500, detail="Error processing response from Gemini API")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error generating video ideas with Gemini API: {response.text}")

def generate_post_content(topic: str, keywords: Optional[str] = None, style: Optional[str] = "engaging") -> str:
    """Generates a YouTube post (text-based) using the Google Gemini API."""
    prompt = f"Generate a YouTube text post about '{topic}' in a '{style}' style."
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
        post_content = result["candidates"][0]["content"]["parts"][0]["text"]
        return post_content
      except (KeyError, IndexError):
          raise HTTPException(status_code=500, detail="Error processing response from Gemini API")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error generating post content with Gemini API: {response.text}")

# --- X (Twitter) Related Functions ---
def generate_tweet(topic: str, keywords: Optional[str] = None, style: Optional[str] = "engaging") -> str:
    """Generates a tweet (text-based) using the Google Gemini API."""
    prompt = f"Generate a concise tweet about '{topic}' in a '{style}' style. Keep it under 280 characters."
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
        tweet = result["candidates"][0]["content"]["parts"][0]["text"]
        return tweet
      except (KeyError, IndexError):
          raise HTTPException(status_code=500, detail="Error processing response from Gemini API")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error generating tweet with Gemini API: {response.text}")

# --- Instagram Related Functions ---
def generate_instagram_post(topic: str, keywords: Optional[str] = None, style: Optional[str] = "engaging") -> str:
    """Generates content for an Instagram post using the Google Gemini API."""
    prompt = f"Generate engaging content for an Instagram post about '{topic}' in a '{style}' style. Include relevant hashtags."
    if keywords:
        prompt += f" Consider these keywords: {keywords}."
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
            post_content = result["candidates"][0]["content"]["parts"][0]["text"]
            return post_content
        except (KeyError, IndexError):
            raise HTTPException(status_code=500, detail="Error processing response from Gemini API")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error generating Instagram post content with Gemini API: {response.text}")

def generate_instagram_story(topic: str, keywords: Optional[str] = None, style: Optional[str] = "engaging") -> str:
    """Generates content for an Instagram story using the Google Gemini API."""
    prompt = f"Generate engaging content for an Instagram story about '{topic}' in a '{style}' style. The content should be concise and attention-grabbing."
    if keywords:
        prompt += f" Consider these keywords: {keywords}."
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
            story_content = result["candidates"][0]["content"]["parts"][0]["text"]
            return story_content
        except (KeyError, IndexError):
            raise HTTPException(status_code=500, detail="Error processing response from Gemini API")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error generating Instagram story content with Gemini API: {response.text}")


def suggest_instagram_channel_name(topic: str, keywords: Optional[str] = None) -> str:
    """Suggests a unique Instagram channel name using the Google Gemini API."""
    prompt = f"Suggest a unique and catchy Instagram channel name about '{topic}'."
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
        raise HTTPException(status_code=response.status_code, detail=f"Error generating Instagram channel name with Gemini API: {response.text}")
        
def generate_instagram_video_ideas(topic: str, keywords: Optional[str] = None) -> str:
    """Generates video ideas for Instagram using the Google Gemini API."""
    prompt = f"Suggest several creative and engaging video ideas for Instagram about '{topic}'."
    if keywords:
        prompt += f" Consider these keywords: {keywords}."
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
            video_ideas = result["candidates"][0]["content"]["parts"][0]["text"]
            return video_ideas
        except (KeyError, IndexError):
            raise HTTPException(status_code=500, detail="Error processing response from Gemini API")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error generating Instagram video ideas with Gemini API: {response.text}")

def suggest_instagram_niche(interests: str) -> str:
    """Suggests a niche for an Instagram channel based on provided interests."""
    prompt = f"""
        You are an expert in identifying profitable and trending niches.

        Based on the following interests: {interests}, suggest several specific Instagram channel niches
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
        raise HTTPException(status_code=response.status_code, detail=f"Error generating Instagram niche suggestions with Gemini API: {response.text}")

def generate_instagram_reel_ideas(topic: str, keywords: Optional[str] = None) -> str:
    """Generates video reel ideas for Instagram using the Google Gemini API."""
    prompt = f"Suggest several creative and engaging video reel ideas for Instagram about '{topic}'. Focus on short, attention-grabbing concepts."
    if keywords:
        prompt += f" Consider these keywords: {keywords}."
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
            reel_ideas = result["candidates"][0]["content"]["parts"][0]["text"]
            return reel_ideas
        except (KeyError, IndexError):
            raise HTTPException(status_code=500, detail="Error processing response from Gemini API")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error generating Instagram reel ideas with Gemini API: {response.text}")

def generate_instagram_video_script(topic: str, style: str) -> str:
    """Generates a script for Instagram videos using the Google Gemini API."""
    payload = {
       "contents": [
        {
          "parts": [
             {
              "text": f"""
              You are an expert script writer who creates high quality video scripts for Instagram.
               
              Generate a video script about '{topic}' in a '{style}' style.
              Make it concise and suitable for a short video.
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
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        try:
          result = response.json()
          script = result["candidates"][0]["content"]["parts"][0]["text"]
          return script
        except (KeyError,IndexError):
          raise HTTPException(status_code=500, detail="Error processing the response from Gemini API")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error generating Instagram video script with Gemini API: {response.text}")

# --- Email Related Functions ---
def generate_email(topic: str, style: str, keywords: Optional[str] = None) -> str:
    """Generates email content using the Google Gemini API."""
    prompt = f"Generate an email about '{topic}' in a '{style}' style."
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
            email_content = result["candidates"][0]["content"]["parts"][0]["text"]
            return email_content
        except (KeyError, IndexError):
            raise HTTPException(status_code=500, detail="Error processing response from Gemini API")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error generating email content with Gemini API: {response.text}")


# --- API Endpoints ---
# YouTube Endpoints
@app.post("/youtube/generate-script", response_model=ScriptResponse)
def generate_video_script(request: ScriptRequest):
    """API endpoint to generate video scripts."""
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required.")
    try:
      script = generate_script(request.topic, request.style)
    except HTTPException as e:
      raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return ScriptResponse(script=script)

@app.post("/youtube/suggest-channel-name", response_model=ChannelNameResponse)
def suggest_youtube_channel_name(request: ChannelNameRequest):
    """API endpoint to suggest a YouTube channel name."""
    if not request.topic:
      raise HTTPException(status_code=400, detail="Topic is required.")
    try:
      channel_name = suggest_channel_name(request.topic, request.keywords)
    except HTTPException as e:
      raise e
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return ChannelNameResponse(channel_name=channel_name)

@app.post("/youtube/suggest-niche", response_model=NicheSuggestionResponse)
def suggest_youtube_niche(request: NicheSuggestionRequest):
    """API endpoint to suggest a YouTube channel niche."""
    if not request.interests:
        raise HTTPException(status_code=400, detail="Interests are required.")
    try:
        niche_suggestions = suggest_niche(request.interests)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return NicheSuggestionResponse(niche_suggestions=niche_suggestions)

@app.post("/youtube/generate-video-ideas", response_model=VideoIdeaResponse)
def generate_youtube_video_ideas(request: VideoIdeaRequest):
    """API endpoint to generate video ideas."""
    if not request.topic:
      raise HTTPException(status_code=400, detail="Topic is required.")
    try:
        video_ideas = generate_video_ideas(request.topic, request.keywords)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return VideoIdeaResponse(video_ideas=video_ideas)

@app.post("/youtube/generate-post-content", response_model=PostContentResponse)
def generate_youtube_post_content(request: PostContentRequest):
    """API endpoint to generate YouTube post content."""
    if not request.topic:
      raise HTTPException(status_code=400, detail="Topic is required.")
    try:
      post_content = generate_post_content(request.topic, request.keywords, request.style)
    except HTTPException as e:
      raise e
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return PostContentResponse(post_content=post_content)

# X (Twitter) Endpoints
@app.post("/x/generate-tweet", response_model=TweetResponse)
def generate_x_tweet(request: TweetRequest):
    """API endpoint to generate tweets."""
    if not request.topic:
      raise HTTPException(status_code=400, detail="Topic is required.")
    try:
      tweet = generate_tweet(request.topic, request.keywords, request.style)
    except HTTPException as e:
      raise e
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return TweetResponse(tweet=tweet)

# Instagram Endpoints
@app.post("/instagram/generate-post", response_model=InstagramPostResponse)
def generate_instagram_post_content(request: InstagramPostRequest):
    """API endpoint to generate Instagram post content."""
    if not request.topic:
      raise HTTPException(status_code=400, detail="Topic is required.")
    try:
      post_content = generate_instagram_post(request.topic, request.keywords, request.style)
    except HTTPException as e:
      raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return InstagramPostResponse(post_content=post_content)

@app.post("/instagram/generate-story", response_model=InstagramStoryResponse)
def generate_instagram_story_content(request: InstagramStoryRequest):
    """API endpoint to generate Instagram story content."""
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required.")
    try:
        story_content = generate_instagram_story(request.topic, request.keywords, request.style)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return InstagramStoryResponse(story_content=story_content)

@app.post("/instagram/suggest-channel-name", response_model=InstagramChannelNameResponse)
def suggest_instagram_channel_name(request: InstagramChannelNameRequest):
    """API endpoint to suggest an Instagram channel name."""
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required.")
    try:
        channel_name = suggest_instagram_channel_name(request.topic, request.keywords)
    except HTTPException as e:
      raise e
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return InstagramChannelNameResponse(channel_name=channel_name)

@app.post("/instagram/generate-video-ideas", response_model=InstagramVideoIdeaResponse)
def generate_instagram_video_ideas(request: InstagramVideoIdeaRequest):
    """API endpoint to generate Instagram video ideas."""
    if not request.topic:
      raise HTTPException(status_code=400, detail="Topic is required.")
    try:
      video_ideas = generate_instagram_video_ideas(request.topic, request.keywords)
    except HTTPException as e:
      raise e
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return InstagramVideoIdeaResponse(video_ideas=video_ideas)

@app.post("/instagram/suggest-niche", response_model=InstagramNicheSuggestionResponse)
def suggest_instagram_niche(request: InstagramNicheSuggestionRequest):
     """API endpoint to suggest Instagram channel niches."""
     if not request.interests:
        raise HTTPException(status_code=400, detail="Interests are required.")
     try:
         niche_suggestions = suggest_instagram_niche(request.interests)
     except HTTPException as e:
         raise e
     except Exception as e:
         raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
     return InstagramNicheSuggestionResponse(niche_suggestions=niche_suggestions)

@app.post("/instagram/generate-reel-ideas", response_model=InstagramReelIdeaResponse)
def generate_instagram_reel_ideas(request: InstagramReelIdeaRequest):
    """API endpoint to generate Instagram reel ideas."""
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required.")
    try:
        reel_ideas = generate_instagram_reel_ideas(request.topic, request.keywords)
    except HTTPException as e:
        raise e
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return InstagramReelIdeaResponse(reel_ideas=reel_ideas)

@app.post("/instagram/generate-video-script", response_model=InstagramVideoScriptResponse)
def generate_instagram_video_script_content(request: InstagramVideoScriptRequest):
    """API endpoint to generate Instagram video script."""
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required.")
    try:
        script = generate_instagram_video_script(request.topic, request.style)
    except HTTPException as e:
        raise e
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return InstagramVideoScriptResponse(script=script)

# Email Endpoints
@app.post("/email/generate-email", response_model=EmailResponse)
def generate_email_content(request: EmailRequest):
    """API endpoint to generate email content."""
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required.")
    try:
        email_content = generate_email(request.topic, request.style, request.keywords)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    return EmailResponse(email_content=email_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)