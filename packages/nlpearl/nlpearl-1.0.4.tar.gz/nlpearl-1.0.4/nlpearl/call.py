# call.py
import requests
import nlpearl

API_URL = "https://api.nlpearl.ai/v1"

class Call:
    @classmethod
    def get_call(cls, call_id):
        if nlpearl.api_key is None:
            raise ValueError("API key is not set. Set the api_key first using 'pearl.api_key = YOUR_API_KEY'")

        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Call/{call_id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @classmethod
    def create_call(cls, to_number, from_number, duration):
        if nlpearl.api_key is None:
            raise ValueError("API key is not set. Set the api_key first using 'pearl.api_key = YOUR_API_KEY'")

        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Call"
        data = {
            "to": to_number,
            "from": from_number,
            "duration": duration
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
