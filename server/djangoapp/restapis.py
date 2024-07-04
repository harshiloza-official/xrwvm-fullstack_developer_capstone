import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

# Setup logging
logger = logging.getLogger(__name__)

def get_request(endpoint, **kwargs):
    params = "&".join(f"{key}={value}" for key, value in kwargs.items())
    request_url = f"{backend_url}{endpoint}?{params}"
    
    logger.info(f"GET from {request_url}")
    
    try:
        response = requests.get(request_url)
        response.raise_for_status()  # Raise HTTPError for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Network exception occurred: {e}")
        return {"error": "Network exception occurred"}

def analyze_review_sentiments(text):
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Network exception occurred: {e}")
        return {"error": "Network exception occurred"}

def post_review(data_dict):
    request_url = f"{backend_url}/insert_review"
    
    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Network exception occurred: {e}")
        return {"error": "Network exception occurred"}
