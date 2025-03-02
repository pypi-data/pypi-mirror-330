import requests
from .config import APIConfig

class APIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get(self, endpoint):
        return requests.get(
            APIConfig.get_url(endpoint),
            headers=self.headers
        )
    
    def post(self, endpoint, data):
        return requests.post(
            APIConfig.get_url(endpoint),
            json=data,
            headers=self.headers
        )