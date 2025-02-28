import requests
import nlpearl  # To access the global api_key
from ._helpers import _process_date

API_URL = "https://api.nlpearl.ai/v1"


class Outbound:
    @classmethod
    def get_all(cls):
        """Get all outbounds."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Outbound"
        response = requests.get(url, headers=headers)
        return response.json()

    @classmethod
    def get(cls, outbound_id):
        """Get a specific outbound by ID."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Outbound/{outbound_id}"
        response = requests.get(url, headers=headers)
        return response.json()

    @classmethod
    def set_active(cls, outbound_id, is_active):
        """Activate or deactivate an outbound."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Outbound/{outbound_id}/Active"
        data = {"isActive": is_active}
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    @classmethod
    def get_calls(cls, outbound_id, from_date, to_date, skip=0, limit=100, sort_prop=None, is_ascending=True,
                  tags=None):
        """
        Get calls for an outbound with optional filters.

        Parameters:
            outbound_id (str): The unique identifier of the outbound.
            from_date: The start date for filtering (required; datetime/date object or ISO 8601 string).
            to_date: The end date for filtering (required; datetime/date object or ISO 8601 string).
            skip (int): Number of entries to skip for pagination.
            limit (int): Limit on the number of entries to return.
            sort_prop (str | None): Property name to sort by.
            is_ascending (bool): Whether the sort order is ascending.
            tags (list[str] | None): List of tags to filter by.

        Returns:
            dict: JSON response from the API (includes error details if any).
        """
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        # Process dates
        from_date_str = _process_date(from_date)
        to_date_str = _process_date(to_date)

        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Outbound/{outbound_id}/Calls"
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

        response = requests.post(url, headers=headers, json=data)
        return response.json()

    @classmethod
    def add_lead(cls, outbound_id, phone_number=None, external_id=None, call_data=None):
        """
        Add a lead to an outbound.

        Parameters:
            outbound_id (str): The unique identifier of the outbound.
            phone_number (str | None): The phone number of the lead.
            external_id (str | None): The external identifier for the lead.
            call_data (dict | None): Additional call data.

        Returns:
            dict: JSON response from the API.
        """
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Outbound/{outbound_id}/Lead"
        data = {}
        if phone_number:
            data["phoneNumber"] = phone_number
        if external_id:
            data["externalId"] = external_id
        if call_data:
            data["callData"] = call_data
        response = requests.put(url, headers=headers, json=data)
        return response.json()

    @classmethod
    def get_leads(cls, outbound_id, skip=0, limit=100, sort_prop=None,
                  is_ascending=True, status=None):
        """
        Get leads for an outbound with optional filters.

        Parameters:
            outbound_id (str): The unique identifier of the outbound.
            skip (int): Number of entries to skip for pagination.
            limit (int): Limit on the number of entries to return.
            sort_prop (str | None): Property name to sort by.
            is_ascending (bool): Whether the sort order is ascending.
            status (int | None): Filter leads by status.

        Returns:
            dict: JSON response from the API.
        """
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Outbound/{outbound_id}/Leads"
        data = {
            "skip": skip,
            "limit": limit,
            "isAscending": is_ascending,
        }
        if sort_prop:
            data["sortProp"] = sort_prop
        if status:
            data["status"] = status
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    @classmethod
    def get_lead_by_id(cls, outbound_id, lead_id):
        """Get a specific lead by lead ID."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Outbound/{outbound_id}/Lead/{lead_id}"
        response = requests.get(url, headers=headers)
        return response.json()

    @classmethod
    def get_lead_by_external_id(cls, outbound_id, external_id):
        """Get a lead by external ID."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Outbound/{outbound_id}/Lead/External/{external_id}"
        response = requests.get(url, headers=headers)
        return response.json()

    @classmethod
    def make_call(cls, outbound_id, to, call_data=None):
        """Make a call in an outbound campaign."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Outbound/{outbound_id}/Call"
        data = {"to": to}
        if call_data:
            data["callData"] = call_data
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    @classmethod
    def get_call_request(cls, request_id):
        """Get details of a specific call request."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Outbound/CallRequest/{request_id}"
        response = requests.get(url, headers=headers)
        return response.json()

    @classmethod
    def get_call_requests(cls, outbound_id, from_date, to_date, skip=0, limit=100, sort_prop=None,
                          is_ascending=True):
        """
        Get call requests for an outbound with optional filters.

        Parameters:
            outbound_id (str): The unique identifier of the outbound.
            from_date: The start date for filtering (required; datetime/date or ISO 8601 string).
            to_date: The end date for filtering (required; datetime/date or ISO 8601 string).
            skip (int): Number of entries to skip for pagination.
            limit (int): Limit on the number of entries to return.
            sort_prop (str | None): Property name to sort by.
            is_ascending (bool): Whether the sort order is ascending.

        Returns:
            dict: JSON response from the API (including error details if any).
        """
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")
        from_date_str = _process_date(from_date)
        to_date_str = _process_date(to_date)
        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Outbound/{outbound_id}/CallRequest"
        data = {
            "skip": skip,
            "limit": limit,
            "isAscending": is_ascending,
            "fromDate": from_date_str,
            "toDate": to_date_str
        }
        if sort_prop:
            data["sortProp"] = sort_prop
        response = requests.post(url, headers=headers, json=data)
        return response.json()
