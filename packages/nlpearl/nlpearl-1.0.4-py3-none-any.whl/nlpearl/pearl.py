import requests
import nlpearl  # To access the global api_key

API_URL = "https://api.nlpearl.ai/v1"


class Pearl:
    @classmethod
    def reset_customer_memory(cls, pearl_id, phone_number):
        """
        Resets stored memory associated with a specific customer's phone number for a given Pearl.

        Endpoint:
            PUT /v1/Pearl/{pearlId}/Memory/{phoneNumber}/Reset

        Parameters:
            pearl_id (str): The unique identifier of the Pearl whose memory should be reset.
            phone_number (str): The phone number associated with the customer whose memory should be reset.

        Returns:
            The response from the API. If the response is in JSON format, returns the parsed JSON;
            otherwise, returns the raw text.
        """
        if nlpearl.api_key is None:
            raise ValueError("API key is not set. Set it using 'pearl.api_key = YOUR_API_KEY'.")

        if not phone_number.startswith("+"):
            phone_number = f"+{phone_number}"

        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Pearl/{pearl_id}/Memory/{phone_number}/Reset"

        response = requests.put(url, headers=headers)
        try:
            return response.json()
        except ValueError:
            return response.text