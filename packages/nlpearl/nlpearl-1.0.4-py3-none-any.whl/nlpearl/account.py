# account.py
import requests
import nlpearl  # Import the main module to access the global api_key

API_URL = "https://api.nlpearl.ai/v1"

class Account:
    @classmethod
    def get_account(cls):
        if nlpearl.api_key is None:
            raise ValueError("API key is not set. Set the api_key first using 'pearl.api_key = YOUR_API_KEY'")

        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Account"
        response = requests.get(url, headers=headers)
        return response.json()

