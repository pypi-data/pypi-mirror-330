import os
import requests
import time
import logging
from sjm.logging_config import setup_logging

# Setup logging
logger = setup_logging()

class SjmAPI:
    """
    SJM API Client for Freelancer Matching & AI-Powered Interviews.
    """

    debug = False  # Global debug mode

    def __init__(self, api_key: str, base_url=None, max_retries=3, timeout=10):
        """
        Initialize the SJM API Client.

        :param api_key: The API key for authentication.
        :param base_url: API base URL (default to Docker-hosted API).
        :param max_retries: Number of times to retry failed requests.
        :param timeout: Timeout for API requests (in seconds).
        """
        self.api_key = api_key
        self.base_url = base_url or os.getenv("SJM_API_URL", "http://141.148.42.161:81/api/v1/docker/")
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        self.max_retries = max_retries
        self.timeout = timeout

    def match_freelancers(self, job_data: dict):
        """Find freelancers based on job details."""
        return self._send_request("POST", "match", json=job_data)

    def test_connection(self):
        """Test API connection."""
        return self._send_request("GET", "health")

    def _send_request(self, method, endpoint, json=None):
        """
        Internal method to send API requests with retries & logging.

        :param method: HTTP method (GET, POST, etc.).
        :param endpoint: API endpoint.
        :param json: Request payload.
        :return: API response or error message.
        """
        url = f"{self.base_url}{endpoint}"
        retries = 0

        while retries < self.max_retries:
            try:
                response = requests.request(method, url, headers=self.headers, json=json, timeout=self.timeout)
                response.raise_for_status()

                # Debug Mode: Print request details
                if SjmAPI.debug:
                    print(f"📡 Request to {url}: {json}")
                    print(f"✅ Response: {response.json()}")

                # Log API request
                logger.info(f"API Request: {method} {url} | Response: {response.status_code}")

                return response.json()

            except requests.exceptions.RequestException as e:
                logger.error(f"API Error [{method} {url}]: {str(e)}")

                if retries < self.max_retries - 1:
                    retries += 1
                    time.sleep(2)  # Wait before retrying
                    logger.warning(f"Retrying... ({retries}/{self.max_retries})")
                else:
                    return {"error": str(e)}

