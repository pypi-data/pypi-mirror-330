import os
import requests

# Auto-detect API endpoint
BASE_URL = os.getenv("SJM_API_URL", "http://141.148.42.161:81/api/v1/docker/")      
def match_freelancers(data, api_key):
    """Send a request to the SJM API for freelancer matching."""
    url = f"{BASE_URL}match"
    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
    response = requests.post(url, json=data, headers=headers)

    try:
        return response.json()
    except Exception:
        return {"error": "Invalid API response"}




