import requests
import nlpearl  # To access the global api_key
from ._helpers import _process_date

API_URL = "https://api.nlpearl.ai/v1"


class Inbound:
    @classmethod
    def get_all(cls):
        """Get all inbounds."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set. Set it using 'pearl.api_key = YOUR_API_KEY'.")
        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Inbound"
        response = requests.get(url, headers=headers)
        return response.json()

    @classmethod
    def get(cls, inbound_id):
        """Get a specific inbound by ID."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Inbound/{inbound_id}"
        response = requests.get(url, headers=headers)
        return response.json()

    @classmethod
    def set_active(cls, inbound_id, is_active):
        """Activate or deactivate an inbound."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Inbound/{inbound_id}/Active"
        data = {"isActive": is_active}
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    @classmethod
    def get_calls(cls, inbound_id, from_date, to_date, skip=0, limit=100, sort_prop=None, is_ascending=True,
                  tags=None, statuses=None, search_input=None):
        """
        Retrieves the calls within a specific date range for an inbound, with additional filters.

        Parameters:
            inbound_id (str): The unique identifier of the inbound configuration.
            from_date: The start date for filtering (required; datetime/date object or ISO 8601 string).
            to_date: The end date for filtering (required; datetime/date object or ISO 8601 string).
            skip (int): Number of entries to skip for pagination.
            limit (int): Limit on the number of entries to return.
            sort_prop (str | None): Property name to sort by.
            is_ascending (bool): Whether the sort order is ascending.
            tags (list[str] | None): List of tags to filter by.
            statuses (list[int] | None): List of status codes to filter by.
            search_input (str | None): Text to filter by.

        Returns:
            dict: JSON response from the API (includes error details if any).
        """
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        # Process the date values using the private helper function.
        from_date_str = _process_date(from_date)
        to_date_str = _process_date(to_date)

        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Inbound/{inbound_id}/Calls"
        data = {
            "skip": skip,
            "limit": limit,
            "isAscending": is_ascending,
            "fromDate": from_date_str,
            "toDate": to_date_str
        }
        if sort_prop:
            data["sortProp"] = sort_prop
        if tags:
            data["tags"] = tags
        if statuses:
            data["statuses"] = statuses
        if search_input:
            data["searchInput"] = search_input

        response = requests.post(url, headers=headers, json=data)
        return response.json()

    @classmethod
    def get_ongoing_calls(cls, inbound_id):
        """
        Retrieves the number of ongoing calls and the number of calls in queue for a specific inbound.

        Endpoint:
            GET /v1/Inbound/{inboundId}/OngoingCalls

        Parameters:
            inbound_id (str): The unique identifier of the inbound.

        Returns:
            dict or str: The response from the API, which should contain:
                - totalOngoingCalls (int): The number of ongoing calls.
                - totalOnQueue (int): The number of calls in queue.
            If the response is not JSON (since it may be text/plain), it will return the raw text.
        """
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Inbound/{inbound_id}/OngoingCalls"
        response = requests.get(url, headers=headers)
        try:
            return response.json()
        except ValueError:
            return response.text