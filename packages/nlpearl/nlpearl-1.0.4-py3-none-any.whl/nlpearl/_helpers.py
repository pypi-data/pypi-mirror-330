import re
from datetime import datetime, date

def _process_date(date_val):
    """
    Processes the date input:
    - If date_val is a string, checks if it matches the ISO 8601 format with a trailing 'Z'.
    - If date_val is a datetime or date object, converts it to an ISO 8601 string with millisecond precision and appends 'Z'.
    """
    iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$'
    if isinstance(date_val, str):
        if not re.match(iso_pattern, date_val):
            raise ValueError(
                f"Date string '{date_val}' does not match required ISO format (e.g., 2025-05-29T13:43:23.939Z)"
            )
        return date_val
    elif isinstance(date_val, (datetime, date)):
        if isinstance(date_val, date) and not isinstance(date_val, datetime):
            date_val = datetime.combine(date_val, datetime.min.time())
        return date_val.isoformat(timespec='milliseconds') + "Z"
    else:
        raise TypeError("The date value must be either a string or a datetime/date object.")
