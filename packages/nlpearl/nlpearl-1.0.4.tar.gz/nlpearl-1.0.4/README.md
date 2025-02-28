# NLPearl Python Wrapper

NLPearl is a Python wrapper for the NLPearl API, allowing developers to interact seamlessly with NLPearl's services from Python applications. This package simplifies the process of integrating NLPearl's powerful conversational AI capabilities into your projects.

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [Usage](#usage)
  - [Account](#account)
  - [Call](#call)
  - [Inbound Operations](#inbound-operations)
  - [Outbound Operations](#outbound-operations)
- [API Reference](#api-reference)
  - [Account](#account-api)
  - [Call](#call-api)
  - [Inbound](#inbound-api)
  - [Outbound](#outbound-api)
- [License](#license)
- [Contact](#contact)

## Installation

Install the package via pip:

```bash
pip install nlpearl
```

## Getting Started

Before using the `nlpearl` package, you need to obtain an API key from NLPearl. You can request one by contacting [Samuel Schwarcz](mailto:samuel@nlpearl.ai).

## Authentication

Set your API key before making any API calls:

```python
import nlpearl as pearl

# Set your API key
pearl.api_key = "your_api_key_here"
```

## Usage

### Account

#### Retrieve Account Information

```python
account_info = pearl.Account.get_account()
print(account_info)
```

### Call

#### Retrieve Call Information

```python
call_id = "your_call_id"
call_info = pearl.Call.get_call(call_id)
print(call_info)
```

### Inbound Operations

#### Get All Inbounds

```python
inbounds = pearl.Inbound.get_all()
print(inbounds)
```

#### Get Specific Inbound

```python
inbound_id = "your_inbound_id"
inbound_info = pearl.Inbound.get(inbound_id)
print(inbound_info)
```

#### Activate or Deactivate Inbound

```python
# Activate
pearl.Inbound.set_active(inbound_id, is_active=True)

# Deactivate
pearl.Inbound.set_active(inbound_id, is_active=False)
```

#### Search Calls in Inbound

```python
inbound_calls = pearl.Inbound.get_calls(
    inbound_id,
    skip=0,
    limit=100,
    sort_prop="date",
    is_ascending=True,
    from_date="2023-11-07T05:31:56Z",
    to_date="2023-11-08T05:31:56Z",
    tags=["tag1", "tag2"]
)
print(inbound_calls)
```

### Outbound Operations

#### Get All Outbounds

```python
outbounds = pearl.Outbound.get_all()
print(outbounds)
```

#### Get Specific Outbound

```python
outbound_id = "your_outbound_id"
outbound_info = pearl.Outbound.get(outbound_id)
print(outbound_info)
```

#### Activate or Deactivate Outbound

```python
# Activate
pearl.Outbound.set_active(outbound_id, is_active=True)

# Deactivate
pearl.Outbound.set_active(outbound_id, is_active=False)
```

#### Add Lead to Outbound

```python
add_lead_response = pearl.Outbound.add_lead(
    outbound_id,
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    phone_number="+1234567890",
    external_id="external123"
)
print(add_lead_response)
```

#### Search Leads in Outbound

```python
leads = pearl.Outbound.get_leads(
    outbound_id,
    skip=0,
    limit=100,
    sort_prop="lastName",
    is_ascending=True,
    status=1  # Replace with the appropriate status code
)
print(leads)
```

#### Get Lead by ID

```python
lead_id = "your_lead_id"
lead_info = pearl.Outbound.get_lead_by_id(outbound_id, lead_id)
print(lead_info)
```

#### Get Lead by External ID

```python
external_id = "your_external_id"
lead_info_external = pearl.Outbound.get_lead_by_external_id(outbound_id, external_id)
print(lead_info_external)
```

#### Make Call in Outbound

```python
call_response = pearl.Outbound.make_call(
    outbound_id,
    to="+1234567890",
    call_data={"firstName": "John", "lastName": "Doe"}
)
print(call_response)
```

#### Get Call Request Details

```python
request_id = "your_request_id"
call_request_info = pearl.Outbound.get_call_request(request_id)
print(call_request_info)
```

#### Search Call Requests in Outbound

```python
call_requests = pearl.Outbound.get_call_requests(
    outbound_id,
    skip=0,
    limit=100,
    sort_prop="date",
    is_ascending=True,
    from_date="2023-11-07T05:31:56Z",
    to_date="2023-11-08T05:31:56Z"
)
print(call_requests)
```

## API Reference

### Account API

#### `pearl.Account.get_account()`

Retrieves account information.

**Response Fields:**

- `name`: The name of the client.
- `totalAgents`: The total number of agents.
- `creditBalance`: The current credit balance.
- `status`: Authorization status for making calls.
  - `1`: FullAccess
  - `2`: LimitedAccess
  - `3`: NoCredits
  - `4`: SuspendedAccount
- `remainingMinutes`: The remaining minutes available.

### Call API

#### `pearl.Call.get_call(call_id)`

Retrieves all the information about a call.

**Parameters:**

- `call_id`: The unique identifier of the call.

**Response Fields:**

- `id`: The unique identifier of the call.
- `relatedId`: The ID of the related activity.
- `startTime`: When the call processing started.
- `conversationStatus`: Outcome of the conversation.
  - `10`: NeedRetry
  - `100`: Success
  - `110`: NotSuccessful
  - `130`: Complete
  - `200`: Error
- `status`: Current status of the call.
  - `3`: InProgress
  - `4`: Completed
  - `5`: Busy
  - `6`: Failed
  - `7`: NoAnswer
  - `8`: Canceled
- `from`: The phone number from which the call was made.
- `to`: The phone number to which the call was made.
- `duration`: Duration of the call in seconds.
- `recording`: URL of the call recording.
- `transcript`: List of chat messages representing the conversation.
- `summary`: Summary of the conversation.
- `collectedInfo`: Information collected during the call.
- `tags`: Tags or labels triggered during the conversation.

### Inbound API

#### `pearl.Inbound.get_all()`

Retrieves all inbounds.

#### `pearl.Inbound.get(inbound_id)`

Retrieves a specific inbound by its ID.

**Parameters:**

- `inbound_id`: The unique identifier of the inbound.

#### `pearl.Inbound.set_active(inbound_id, is_active)`

Activates or deactivates a specific inbound.

**Parameters:**

- `inbound_id`: The unique identifier of the inbound.
- `is_active`: `True` to activate, `False` to deactivate.

#### `pearl.Inbound.get_calls(...)`

Retrieves the calls within a specific date range of inbound.

**Parameters:**

- `inbound_id`: The unique identifier of the inbound.
- `skip`: Number of entries to skip for pagination.
- `limit`: Limit on the number of entries to return.
- `sort_prop`: Property name to sort by.
- `is_ascending`: Whether the sort order is ascending.
- `from_date`: The start date for filtering.
- `to_date`: The end date for filtering.
- `tags`: List of tags to filter by.

### Outbound API

#### `pearl.Outbound.get_all()`

Retrieves all outbounds.

#### `pearl.Outbound.get(outbound_id)`

Retrieves a specific outbound by its ID.

**Parameters:**

- `outbound_id`: The unique identifier of the outbound.

#### `pearl.Outbound.set_active(outbound_id, is_active)`

Activates or deactivates a specific outbound.

**Parameters:**

- `outbound_id`: The unique identifier of the outbound.
- `is_active`: `True` to activate, `False` to deactivate.

#### `pearl.Outbound.get_calls(...)`

Retrieves the calls within a specific date range for a given outbound.

**Parameters:**

- `outbound_id`: The unique identifier of the outbound.
- `skip`: Number of entries to skip for pagination.
- `limit`: Limit on the number of entries to return.
- `sort_prop`: Property name to sort by.
- `is_ascending`: Whether the sort order is ascending.
- `from_date`: The start date for filtering.
- `to_date`: The end date for filtering.
- `tags`: List of tags to filter by.

#### `pearl.Outbound.add_lead(...)`

Adds a new lead to a specified outbound.

**Parameters:**

- `outbound_id`: The unique identifier of the outbound.
- `first_name`: The first name of the lead.
- `last_name`: The last name of the lead.
- `email`: The email address of the lead.
- `phone_number`: The phone number of the lead.
- `external_id`: An optional external identifier for the lead.

#### `pearl.Outbound.get_leads(...)`

Retrieves the leads associated with a specific outbound.

**Parameters:**

- `outbound_id`: The unique identifier of the outbound.
- `skip`: Number of entries to skip for pagination.
- `limit`: Limit on the number of entries to return.
- `sort_prop`: Property name to sort by.
- `is_ascending`: Whether the sort order is ascending.
- `status`: Status code to filter leads.

**Lead Status Codes:**

- `1`: New
- `10`: NeedRetry
- `40`: OnCall
- `100`: Success
- `110`: NotSuccessful
- `130`: Complete
- `500`: Error

#### `pearl.Outbound.get_lead_by_id(outbound_id, lead_id)`

Retrieves details of a specific lead within an outbound.

**Parameters:**

- `outbound_id`: The unique identifier of the outbound.
- `lead_id`: The unique identifier of the lead.

#### `pearl.Outbound.get_lead_by_external_id(outbound_id, external_id)`

Retrieves a lead by its external ID.

**Parameters:**

- `outbound_id`: The unique identifier of the outbound.
- `external_id`: The external identifier of the lead.

#### `pearl.Outbound.make_call(outbound_id, to, call_data=None)`

Initiates an outbound phone call associated with the specified outbound ID.

**Parameters:**

- `outbound_id`: The unique identifier of the outbound.
- `to`: The phone number to which the call will be made.
- `call_data`: A dictionary containing additional information about the call.

#### `pearl.Outbound.get_call_request(request_id)`

Fetches detailed information about a specific API call request.

**Parameters:**

- `request_id`: The unique identifier of the API request.

#### `pearl.Outbound.get_call_requests(...)`

Retrieves a list of API call requests associated with a specific outbound.

**Parameters:**

- `outbound_id`: The unique identifier of the outbound.
- `skip`: Number of entries to skip for pagination.
- `limit`: Limit on the number of entries to return.
- `sort_prop`: Property name to sort by.
- `is_ascending`: Whether the sort order is ascending.
- `from_date`: The start date for filtering.
- `to_date`: The end date for filtering.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact:

- **Support NLPearl**
- Email: [support@nlpearl.ai](mailto:support@nlpearl.ai)
