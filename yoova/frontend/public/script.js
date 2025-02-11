document.addEventListener('DOMContentLoaded', () => {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    function activateTab(tabId) {
        tabContents.forEach(content => {
            content.classList.remove('active');
        });
        tabButtons.forEach(button => {
            button.classList.remove('active');
        });
        document.getElementById(tabId).classList.add('active');
        document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
    }

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.dataset.tab;
            activateTab(tabId);
        });
    });

    const API_BASE_URL = "http://127.0.0.1:8000"; // Base URL for your backend API

    // --- YouTube Functions ---
    document.getElementById('generateScript').addEventListener('click', () => {
        const topic = document.getElementById('youtubeTopic').value;
        const style = document.getElementById('youtubeStyle').value;
        fetch(`${API_BASE_URL}/youtube/generate-script`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, style: style || "informative" }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('youtubeOutput').innerText = data.script;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('youtubeOutput').innerText = 'Error generating script.';
            });
    });

    document.getElementById('suggestChannelName').addEventListener('click', () => {
        const topic = document.getElementById('youtubeTopic').value;
        const keywords = document.getElementById('youtubeKeywords').value;

        fetch(`${API_BASE_URL}/youtube/suggest-channel-name`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, keywords: keywords || null }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('youtubeOutput').innerText = data.channel_name;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('youtubeOutput').innerText = 'Error suggesting channel name.';
            });
    });

    document.getElementById('suggestNiche').addEventListener('click', () => {
        const interests = document.getElementById('youtubeTopic').value;
        fetch(`${API_BASE_URL}/youtube/suggest-niche`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ interests: interests }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('youtubeOutput').innerText = data.niche_suggestions;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('youtubeOutput').innerText = 'Error suggesting a niche.';
            });
    });

    document.getElementById('generateVideoIdeas').addEventListener('click', () => {
        const topic = document.getElementById('youtubeTopic').value;
        const keywords = document.getElementById('youtubeKeywords').value;

        fetch(`${API_BASE_URL}/youtube/generate-video-ideas`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, keywords: keywords || null }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('youtubeOutput').innerText = data.video_ideas;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('youtubeOutput').innerText = 'Error generating video ideas.';
            });
    });

    document.getElementById('generatePostContent').addEventListener('click', () => {
        const topic = document.getElementById('youtubeTopic').value;
        const keywords = document.getElementById('youtubeKeywords').value;
        const style = document.getElementById('youtubeStyle').value;

        fetch(`${API_BASE_URL}/youtube/generate-post-content`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, keywords: keywords || null, style: style || "engaging" }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('youtubeOutput').innerText = data.post_content;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('youtubeOutput').innerText = 'Error generating post content.';
            });
    });


    // --- X (Twitter) Functions ---
    document.getElementById('generateTweet').addEventListener('click', () => {
        const topic = document.getElementById('xTopic').value;
        const keywords = document.getElementById('xKeywords').value;
        const style = document.getElementById('xStyle').value;
        fetch(`${API_BASE_URL}/x/generate-tweet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, keywords: keywords || null, style: style || "engaging" }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('xOutput').innerText = data.tweet;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('xOutput').innerText = 'Error generating tweet.';
            });
    });


    // --- Instagram Functions ---
    document.getElementById('generateInstagramPost').addEventListener('click', () => {
        const topic = document.getElementById('instagramTopic').value;
        const keywords = document.getElementById('instagramKeywords').value;
        const style = document.getElementById('instagramStyle').value;
        fetch(`${API_BASE_URL}/instagram/generate-post`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, keywords: keywords || null, style: style || "engaging" }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('instagramOutput').innerText = data.post_content;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('instagramOutput').innerText = 'Error generating Instagram post content.';
            });
    });

    document.getElementById('generateInstagramStory').addEventListener('click', () => {
        const topic = document.getElementById('instagramTopic').value;
        const keywords = document.getElementById('instagramKeywords').value;
        const style = document.getElementById('instagramStyle').value;
        fetch(`${API_BASE_URL}/instagram/generate-story`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, keywords: keywords || null, style: style || "engaging" }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('instagramOutput').innerText = data.story_content;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('instagramOutput').innerText = 'Error generating Instagram story content.';
            });
    });

    document.getElementById('suggestInstagramChannelName').addEventListener('click', () => {
        const topic = document.getElementById('instagramTopic').value;
        const keywords = document.getElementById('instagramKeywords').value;

        fetch(`${API_BASE_URL}/instagram/suggest-channel-name`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, keywords: keywords || null }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('instagramOutput').innerText = data.channel_name;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('instagramOutput').innerText = 'Error suggesting Instagram channel name.';
            });
    });

    document.getElementById('generateInstagramVideoIdeas').addEventListener('click', () => {
        const topic = document.getElementById('instagramTopic').value;
        const keywords = document.getElementById('instagramKeywords').value;

        fetch(`${API_BASE_URL}/instagram/generate-video-ideas`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, keywords: keywords || null }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('instagramOutput').innerText = data.video_ideas;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('instagramOutput').innerText = 'Error generating Instagram video ideas.';
            });
    });

    document.getElementById('suggestInstagramNiche').addEventListener('click', () => {
        const interests = document.getElementById('instagramTopic').value;
        fetch(`${API_BASE_URL}/instagram/suggest-niche`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ interests: interests }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('instagramOutput').innerText = data.niche_suggestions;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('instagramOutput').innerText = 'Error suggesting Instagram niche.';
            });
    });

    document.getElementById('generateInstagramReelIdeas').addEventListener('click', () => {
        const topic = document.getElementById('instagramTopic').value;
        const keywords = document.getElementById('instagramKeywords').value;
        fetch(`${API_BASE_URL}/instagram/generate-reel-ideas`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, keywords: keywords || null }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('instagramOutput').innerText = data.reel_ideas;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('instagramOutput').innerText = 'Error generating Instagram reel ideas.';
            });
    });

    document.getElementById('generateInstagramVideoScript').addEventListener('click', () => {
        const topic = document.getElementById('instagramTopic').value;
        const style = document.getElementById('instagramStyle').value;
        fetch(`${API_BASE_URL}/instagram/generate-video-script`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, style: style || "informative" }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('instagramOutput').innerText = data.script;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('instagramOutput').innerText = 'Error generating Instagram video script.';
            });
    });


    // --- Email Functions ---
    document.getElementById('generateEmail').addEventListener('click', () => {
        const topic = document.getElementById('emailTopic').value;
        const style = document.getElementById('emailStyle').value;
        const keywords = document.getElementById('emailKeywords').value;
        fetch(`${API_BASE_URL}/email/generate-email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, style: style || "professional", keywords: keywords || null }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('emailOutput').innerText = data.email_content;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('emailOutput').innerText = 'Error generating email.';
            });
    });
});