# 3X-UI python Client Documentation

---
### Note:
Examples of response data can be found at this [link](https://www.postman.com/hsanaei/3x-ui/collection/q1l5l0u/3x-ui).

---

# Payloads

## Class: `Payload`

The `Payload` class is base class for all other payloads, designed to handle a dictionary as its data source,
format nested dictionaries into JSON strings,
and provide clear and concise string representations for easy debugging.
---

### Constructor

```python
Payload(data: dict)
```

#### Parameters:
- `data` (`dict`): A dictionary containing the data to be managed and formatted by the `Payload` instance.

---

### Methods

#### `format()`

Formats the payload by serializing any nested dictionaries into JSON strings.\
**This method will be called before sending a post request.**

```python
def format(self) -> dict
```

#### Returns:
- A dictionary with nested dictionaries serialized as JSON strings.

#### Example:
```python
data = {
    "user": {"id": 1, "name": "Alice"},
    "active": True,
    "score": 95
}
payload = Payload(data)
formatted = payload.format()
print(formatted)
# Output: {'user': '{"id": 1, "name": "Alice"}', 'active': True, 'score': 95}
```
---


## Class: `ClientPayload`

### Description

The `ClientPayload` class generates structured payloads for managing inbound client configurations in panel.

It supports customizable parameters such as client ID, email, traffic limits, and additional optional fields.

The class inherits from the `Payload` base class.

---

### Constructor

```python
ClientPayload(
    inbound_id: int,
    client_id: str,
    email: str,
    limitip: int,
    expiry_time: float,
    subid: str,
    flow: str = "xtls-rprx-vision",
    total_gb: int = 0,
    enable: bool = True,
    reset: int = 0,
    additional_fields: Optional[dict] = None
)
```

#### Parameters:
- `inbound_id` (`int`): The ID of the inbound connection.
- `client_id` (`str`): The unique identifier for the client.
- `email` (`str`): The email address associated with the client.
- `limitip` (`int`): Maximum simultaneous IP connections allowed.
- `expiry_time` (`float`): Timestamp for when the client's access expires.
- `subid` (`str`): Subscription ID for the client.
- `flow` (`str`, optional): Flow setting for the client. Defaults to `"xtls-rprx-vision"`.
- `total_gb` (`int`, optional): Total allowed traffic in gigabytes. Defaults to `0` (unlimited).
- `enable` (`bool`, optional): Whether the client is enabled. Defaults to `True`.
- `reset` (`int`, optional): Reset interval for traffic statistics. Defaults to `0`.
- `additional_fields` (`dict`, optional): Additional fields to include in the client settings. Defaults to `None`.

---

### Methods

#### `format()`

Returns a right-formatted payload for POST requests

---

### Example Usage:
```python
payload = ClientPayload(
    inbound_id=123,
    client_id="abcd1234",
    email="client@example.com",
    limitip=5,
    expiry_time=1700000000,
    subid="sub-001"
)
print(str(payload))
# Output:
# ClientPayload:
# Inbound: 123,
# Settings: {'clients': [{'id': 'abcd1234', 'flow': 'xtls-rprx-vision', 'email': 'client@example.com',
#                         'limitIp': 5, 'totalGB': 0, 'expiryTime': 1700000000, 'enable': True,
#                         'subId': 'sub-001', 'reset': 0}]}
```

---
### Methods

#### `format()`

Returns a right-formatted payload for POST requests

---

### Notes

- This class automatically handles the serialization of nested dictionaries and ensures all client-related settings are structured for easy integration with VPN or proxy service APIs.
- Any additional fields can be included using the `additional_fields` parameter, making the payload highly flexible.

---

## Class: InboundPayload

The `InboundPayload` class is used to create payloads for managing inbound connections.
It supports detailed customization of parameters such as 
port, stream settings, traffic limits, and protocol settings.

---

### Constructor

```python
InboundPayload(
    port: int,
    stream_settings: dict,
    up: int = 0,
    down: int = 0,
    total: int = 0,
    remark: str = "New",
    enable: bool = True,
    expiry_time: int = 0,
    listen: str = "",
    protocol: str = "vless",
    settings: Optional[dict] = None,
    sniffing: Optional[dict] = None,
    allocate: Optional[dict] = None
)
```

#### Parameters:
- **`port` (`int`)**: The port number for the inbound connection.
- **`stream_settings` (`dict`)**: Configuration for stream settings.
- **`up` (`int`, optional)**: The total uploaded traffic in bytes (default is `0`).
- **`down` (`int`, optional)**: The total downloaded traffic in bytes (default is `0`).
- **`total` (`int`, optional)**: The total allowed traffic in bytes (default is `0`).
- **`remark` (`str`, optional)**: A remark or description for the inbound connection (default is `"New"`).
- **`enable` (`bool`, optional)**: Whether the inbound connection is enabled (default is `True`).
- **`expiry_time` (`int`, optional)**: The timestamp when the inbound connection expires (default is `0`).
- **`listen` (`str`, optional)**: The IP address to listen on (default is an empty string).
- **`protocol` (`str`, optional)**: The protocol for the inbound connection (default is `"vless"`).
- **`settings` (`dict`, optional)**: Additional settings for the inbound connection. If not provided, default settings will be used.
- **`sniffing` (`dict`, optional)**: Configuration for traffic sniffing. If not provided, default sniffing settings will be used.
- **`allocate` (`dict`, optional)**: Configuration for connection allocation. If not provided, default allocation settings will be used.

---



### Example Usage

```py
from client3x import InboundPayload

# Create an InboundPayload object
inbound_payload = InboundPayload(
    port=12345,
    stream_settings={
        "network": "tcp",
        "security": "tls",
        "tlsSettings": {"alpn": ["http/1.1"]}
    },
    up=1000000,
    down=500000,
    total=1000000000,
    remark="Test Inbound",
    enable=True,
    expiry_time=1700000000,
    protocol="vless",
    settings={
        "clients": [{"id": "unique-client-id", "flow": "xtls-rprx-vision"}],
        "decryption": "none",
        "fallbacks": []
    }
)

# Print the payload
print(inbound_payload)

# Access the formatted payload
formatted_payload = inbound_payload.format()
print(formatted_payload)
```

---

### Methods


#### `format()`

Returns a right-formatted payload for POST requests

---

### Notes

- The `InboundPayload` class simplifies the creation of inbound configuration payloads
for use in VPN and proxy services.
- Default values are provided for optional parameters to streamline the setup process.
- Custom configurations for `settings`, `sniffing`, and `allocate` can be included to tailor the payload to specific requirements.


# Clients

## Class: `Client3XUI`


The `Client3XUI` class provides a client interface for managing inbound and client configurations through a panel.\
It facilitates interaction with the panel API,  enabling operations such as retrieving, adding, updating, and deleting inbounds and clients.\
It supports logging, session management, and error handling, offering a comprehensive solution for managing inbounds, clients, and traffic data.

---

### Constructor

```python
Client3XUI(
    login: str,
    password: str,
    login_key: str,
    panel_host: str,
    root_url: str,
    sub_host: str,
    sub_path: str,
    inbound_id: int,
    panel_port: Optional[int] = None,
    sub_port: Optional[int] = None,
    logging_enabled: bool = False
)
```

#### Parameters:
- **`login` (`str`)**: Username for the panel login.
- **`password` (`str`)**: Password for the panel login.
- **`login_key` (`str`)**: Login secret key for authentication.
- **`panel_host` (`str`)**: The host address of the panel.
- **`root_url` (`str`)**: The root URL of the panel.
- **`sub_host` (`str`)**: The host address for subscription services.
- **`sub_path` (`str`)**: The path for subscription services.
- **`inbound_id` (`int`)**: The default inbound ID to use for operations.
- **`panel_port` (`Optional[int]`, optional)**: Port for the panel (default is `None`).
- **`sub_port` (`Optional[int]`, optional)**: Port for subscription services (default is `None`).
- **`logging_enabled` (`bool`, optional)**: Enables logging if set to `True` (default is `False`).

---

### Attributes

- **`inbound` (`int`)**: Stores the default inbound ID.
- **`session` (`Session | None`)**: Manages the client session.
- **`login_payload` (`dict`)**: Contains login credentials and secrets for authentication.
- **`base_url` (`str`)**: Constructs the base URL for panel API requests.
- **`sub_url` (`str`)**: Constructs the subscription service URL.
- **`logger` (`Logger | None`)**: Handles logging if logging is enabled.

---

### Methods

### Session Management

#### Method `__get_session() -> Session`

Establishes and authenticates a session with the panel.

---

### HTTP Requests

#### Method  `__post_request(url: str, payload: Payload | None) -> Response`

Sends a POST request to the specified URL with the given payload.

> **Private Method:** Used internally to handle POST requests.

**Parameters:**
- `url` (`str`): The target URL for the POST request.
- `payload` (`Payload | None`): The data to include in the POST request body.

**Returns:**
- `Response`: The server's response to the POST request.

---

#### Method  `__get_request(url: str) -> Response`

Sends a GET request to the specified URL.

> **Private Method:** Used internally to handle GET requests.

**Parameters:**
- `url` (`str`): The target URL for the GET request.

**Returns:**
- `Response`: The server's response to the GET request.

---

### Inbound Operations

#### Method  `get_inbounds() -> PanelResponse`

Retrieves a list of inbounds from the panel.

```python
response = client.get_inbounds()
```

**Returns:**
- `PanelResponse`: Contains the list of inbounds and their details.

---

#### Method  `online_clients() -> PanelResponse`

Returns a list of currently online clients.

```python
response = client.online_clients()
```

**Returns:**
- `PanelResponse`: A list of active clients connected to the inbounds.

---

#### Method  `reset_all_traffics()`

Resets traffic data for all clients across all inbounds.

```python
client.reset_all_traffics()
```

---

#### Method  `create_backup()`

Creates a backup of the panel configuration.

```python
client.create_backup()
```

---

### Inbound Management

#### Method  `add_inbound(inbound_payload: InboundPayload) -> PanelResponse`

Adds a new inbound to the panel.

```python
response = client.add_inbound(inbound_payload)
```

**Parameters:**
- `inbound_payload` (`InboundPayload`): The configuration details for the new inbound.

**Returns:**
- `PanelResponse`: Contains the result of the addition operation.

---

#### Method  `get_inbound(inbound_id: Optional[int] = None) -> PanelResponse`

Retrieves details of a specific inbound.

```python
response = client.get_inbound(inbound_id=1234)
```

**Parameters:**
- `inbound_id` (`int`, optional): The ID of the inbound to retrieve. Defaults to `None`.

**Returns:**
- `PanelResponse`: Details of the specified inbound.

---

#### Method  `update_inbound(inbound_payload: InboundPayload, inbound_id: Optional[int] = None) -> PanelResponse`

Updates an inbound's configuration.

```python
response = client.update_inbound(inbound_payload, inbound_id=1234)
```

**Parameters:**
- `inbound_payload` (`InboundPayload`): Updated configuration details.
- `inbound_id` (`int`, optional): The ID of the inbound to update. Defaults to `None`.

**Returns:**
- `PanelResponse`: Result of the update operation.

---

#### Method  `delete_inbound(inbound_id: Optional[int] = None)`

Deletes an inbound.

```python
client.delete_inbound(inbound_id=1234)
```

**Parameters:**
- `inbound_id` (`int`, optional): The ID of the inbound to delete. Defaults to `None`.

---

#### Method  `reset_all_clients_in_inbound(inbound_id: Optional[int] = None)`

Resets traffic data for all clients in the specified inbound.

```python
client.reset_all_clients_in_inbound(inbound_id=1234)
```

**Parameters:**
- `inbound_id` (`int`, optional): The ID of the inbound. Defaults to `None`.

---

#### Method  `delete_depleted_clients(inbound_id: Optional[int] = None)`

Deletes clients with expired keys in the specified inbound.

```python
client.delete_depleted_clients(inbound_id=1234)
```

**Parameters:**
- `inbound_id` (`int`, optional): The ID of the inbound. Defaults to `None`.

---

#### Method  `get_clients_in_inbound(inbound_id: Optional[int] = None) -> list`

Retrieves a list of clients in the specified inbound.

```python
clients = client.get_clients_in_inbound(inbound_id=1234)
```

**Parameters:**
- `inbound_id` (`int`, optional): The ID of the inbound. Defaults to `None`.

**Returns:**
- `list`: A list of clients in the specified inbound.

---

### Client Management

#### Method `get_client_traffic(email: str) -> PanelResponse`

Retrieves traffic data for a client by email.

```python
traffic = client.get_client_traffic(email="client@example.com")
```

**Parameters:**
- `email` (`str`): The email of the client.

**Returns:**
- `PanelResponse`: Traffic data for the client.

---

#### Method `get_client_traffic_by_id(client_id: str) -> PanelResponse`

Retrieves traffic data for a client by ID.

```python
traffic = client.get_client_traffic_by_id(client_id="client1234")
```

**Parameters:**
- `client_id` (`str`): The unique ID of the client.

**Returns:**
- `PanelResponse`: Traffic data for the client.

---

#### Method `add_client(payload: ClientPayload) -> str`

Adds a client to the specified inbound and returns a subscription link.

```python
link = client.add_client(payload)
```

**Parameters:**
- `payload` (`ClientPayload`): The details of the client to add.

**Returns:**
- `str`: A subscription link for the new client.

---

#### Method `update_client(client_id: str, payload: ClientPayload) -> str`

Updates a client's details and returns a subscription link.

```python
link = client.update_client(client_id="client1234", payload=updated_payload)
```

**Parameters:**
- `client_id` (`str`): The unique ID of the client.
- `payload` (`ClientPayload`): The updated details for the client.

**Returns:**
- `str`: A subscription link for the updated client.

---

#### Method `delete_client(client_id: str, inbound_id: Optional[int] = None)`

Deletes a client by ID.

```python
client.delete_client(client_id="client1234")
```

**Parameters:**
- `client_id` (`str`): The unique ID of the client.
- `inbound_id` (`int`, optional): The ID of the inbound. Defaults to `None`.

---

#### Method `client_ipaddress(email: str) -> PanelResponse`

Retrieves a client's IP address.

```python
ip = client.client_ipaddress(email="client@example.com")
```

**Parameters:**
- `email` (`str`): The email of the client.

**Returns:**
- `PanelResponse`: The client's IP address.

---

#### Method `clear_client_ipadresses(email: str)`

Clears a client's IP addresses.

```python
client.clear_client_ipadresses(email="client@example.com")
```

**Parameters:**
- `email` (`str`): The email of the client.

---

#### Method `reset_client_traffic(email: str, inbound_id: Optional[int] = None)`

Resets a client's traffic data.

```python
client.reset_client_traffic(email="client@example.com", inbound_id=1234)
```

**Parameters:**
- `email` (`str`): The email of the client.
- `inbound_id` (`int`, optional): The ID of the inbound. Defaults to `None`.

---

### Options
#### Method `__check_inbound(self, inbound_id: int | None) -> int:`
Check if the given inbound_id is None and return self.inbound if it is. Otherwise, log a warning and return the given inbound_id.

**Parameters:**
- `inbound_id` (`int`, optional): The ID of the inbound. Defaults to `None`.
---

### Example Usage

```python
from client3x import Client3XUI

# Initialize the client
client = Client3XUI(
    login="admin",
    password="password",
    login_key="secret",
    panel_host="example.com",
    root_url="api",
    sub_host="sub.example.com",
    sub_path="subscriptions",
    inbound_id=1,
    logging_enabled=True
)

# Retrieve inbounds
inbounds = client.get_inbounds()
print(inbounds)

# Add a new client
from payloads import ClientPayload

payload = ClientPayload(email="user@example.com", uuid="unique-id")
sublink = client.add_client(payload)
print(sublink)

# Reset traffic for a specific client
client.reset_client_traffic(email="user@example.com")
```

---

### Notes
- The `Client3XUI` class ensures proper session management and error handling for robust panel interaction.
- Logging is optional but recommended for debugging and monitoring operations.
- By default, the client works with a specific `Inbound`, but if there are several `Inbounds` in your dashboard, then you can access them by their id.
First make sure that such an inbound exists.
---


## Class: `AsyncClient3XUI`

`AsyncClient3XUI` is an asynchronous client interface for managing inbound and client configurations through a panel.\
It facilitates interaction with the panel API,  enabling operations such as retrieving, adding, updating, and deleting inbounds and clients.\
It supports logging, session management, and error handling, offering a comprehensive solution for managing inbounds, clients, and traffic data.

This class facilitates interaction with a control panel and subscription URLs, with built-in support for logging and customizable configurations.

### Features
- Automatic login and session management.
- Periodic cookie updates with customizable timeout.
- Configurable logging for debugging and monitoring.
- Flexible URL and port configurations for panel and subscription endpoints.

---
Вот документация, оформленная в том же стиле, для вашего класса `AsyncClient3XUI`:

---

# AsyncClient3XUI

`AsyncClient3XUI` is an asynchronous client for managing session cookies and periodically updating them from a server. The client is designed for seamless integration with a control panel and subscription services.

---

## Features

- **Automated Session Management:** Handles login and retrieves session cookies.
- **Periodic Cookie Refresh:** Automatically refreshes cookies at a configurable interval.
- **Logging Support:** Optional logging for debugging and monitoring purposes.
- **Flexible Configuration:** Customizable host, ports, and API paths.

---

### Constructor

```python
AsyncClient3XUI(
    login: str,
    password: str,
    login_key: str,
    panel_host: str,
    root_url: str,
    sub_host: str,
    sub_path: str,
    inbound_id: int,
    panel_port: Optional[int] = None,
    sub_port: Optional[int] = None,
    logging_enabled: bool = False,
    timeout: int = 300
)
```

Initializes an instance of the `AsyncClient3XUI` class.  

#### Parameters:
- **`login`** (`str`):  
  The username for authentication.

- **`password`** (`str`):  
  The password for authentication.

- **`login_key`** (`str`):  
  The login secret key for additional security.

- **`panel_host`** (`str`):  
  Hostname of the control panel server.

- **`root_url`** (`str`):  
  The API root path for the control panel.

- **`sub_host`** (`str`):  
  Hostname of the subscription server.

- **`sub_path`** (`str`):  
  API path for the subscription server.

- **`inbound_id`** (`int`):  
  The identifier for inbound connections.

- **`panel_port`** (`int`, optional):  
  Port for the control panel server. Defaults to `None`.

- **`sub_port`** (`int`, optional):  
  Port for the subscription server. Defaults to `None`.

- **`logging_enabled`** (`bool`, optional):  
  Enables or disables logging for debugging purposes. Defaults to `False`.

- **`timeout`** (`int`, optional):  
  Interval in seconds for refreshing cookies. Defaults to `300`.


### Attributes

- **`inbound`** (`int`):  
  ID of the current inbound connection.

- **`login_payload`** (`dict`):  
  Authentication parameters containing:
  - `username`: The username for authentication.
  - `password`: The password for authentication.
  - `loginSecret`: The login secret key for additional security.

- **`base_url`** (`str`):  
  The base URL of the control panel, constructed from `panel_host`, `panel_port`, and `root_url`.

- **`sub_url`** (`str`):  
  The subscription URL, constructed from `sub_host`, `sub_port`, and `sub_path`.

- **`logger`** (`Logger | None`):  
  A logger instance for recording events. Enabled when `logging_enabled` is set to `True`.

- **`cookie`** (`Any | None`):  
  The current cookies used for authentication.

- **`timeout`** (`int`):  
  The interval in seconds for refreshing cookies.

- **`task`** (`asyncio.Task | None`):  
  The asynchronous task for periodically updating cookies. Created when `start()` is called.

---

## Usage example

```python
import asyncio
from client3x import AsyncClient3XUI

async def main():
    client = AsyncClient3XUI(
        login="admin",
        password="securepass",
        login_key="secretKey123",
        panel_host="api.myservice.com",
        root_url="v1",
        sub_host="subs.myservice.com",
        sub_path="subs",
        inbound_id=1001,
        logging_enabled=True,
        timeout=120
    )

    await client.start()
    print("Client started with periodic cookie updates.")
    # Perform other tasks...
    # The background task will run until the client is deleted or the program ends.

asyncio.run(main())
```

---

### Methods

#### Method `start()`

Starts the background task for periodic cookie updates.

```python
await client.start()
```

---

### Session Management

#### Method  `__del__()`

Closes the session upon object destruction.  
This method is called automatically when the `AsyncClient3XUI` object is deleted.

```python
del client
```

#### Method  `update_cookies_periodically()`

Periodically fetches new cookies from the server based on the configured `timeout`.

> **Note:** This method is called internally by `start()` and should not be called directly.

---

#### Method  `__fetch_cookies()`

Performs a POST request to the `/login` endpoint to authenticate and retrieve cookies.

> **Private Method:** Used internally to handle cookie updates.

---

### HTTP Requests

#### Method  `__post_request(url: str, payload: Payload | None) -> Response`

Sends a POST request to the specified URL with the given payload.

> **Private Method:** Used internally to handle POST requests.

**Parameters:**
- `url` (`str`): The target URL for the POST request.
- `payload` (`Payload | None`): The data to include in the POST request body.

**Returns:**
- `Response`: The server's response to the POST request.

---

#### Method  `__get_request(url: str) -> Response`

Sends a GET request to the specified URL.

> **Private Method:** Used internally to handle GET requests.

**Parameters:**
- `url` (`str`): The target URL for the GET request.

**Returns:**
- `Response`: The server's response to the GET request.

---

### Inbound Operations

#### Method  `get_inbounds() -> PanelResponse`

Retrieves a list of inbounds from the panel.

```python
response = await client.get_inbounds()
```

**Returns:**
- `PanelResponse`: Contains the list of inbounds and their details.

---

#### Method  `online_clients() -> PanelResponse`

Returns a list of currently online clients.

```python
response = await client.online_clients()
```

**Returns:**
- `PanelResponse`: A list of active clients connected to the inbounds.

---

#### Method  `reset_all_traffics()`

Resets traffic data for all clients across all inbounds.

```python
await client.reset_all_traffics()
```

---

#### Method  `create_backup()`

Creates a backup of the panel configuration.

```python
await client.create_backup()
```

---

### Inbound Management

#### Method  `add_inbound(inbound_payload: InboundPayload) -> PanelResponse`

Adds a new inbound to the panel.

```python
response = await client.add_inbound(inbound_payload)
```

**Parameters:**
- `inbound_payload` (`InboundPayload`): The configuration details for the new inbound.

**Returns:**
- `PanelResponse`: Contains the result of the addition operation.

---

#### Method  `get_inbound(inbound_id: Optional[int] = None) -> PanelResponse`

Retrieves details of a specific inbound.

```python
response = await client.get_inbound(inbound_id=1234)
```

**Parameters:**
- `inbound_id` (`int`, optional): The ID of the inbound to retrieve. Defaults to `None`.

**Returns:**
- `PanelResponse`: Details of the specified inbound.

---

#### Method  `update_inbound(inbound_payload: InboundPayload, inbound_id: Optional[int] = None) -> PanelResponse`

Updates an inbound's configuration.

```python
response = await client.update_inbound(inbound_payload, inbound_id=1234)
```

**Parameters:**
- `inbound_payload` (`InboundPayload`): Updated configuration details.
- `inbound_id` (`int`, optional): The ID of the inbound to update. Defaults to `None`.

**Returns:**
- `PanelResponse`: Result of the update operation.

---

#### Method  `delete_inbound(inbound_id: Optional[int] = None)`

Deletes an inbound.

```python
await client.delete_inbound(inbound_id=1234)
```

**Parameters:**
- `inbound_id` (`int`, optional): The ID of the inbound to delete. Defaults to `None`.

---

#### Method  `reset_all_clients_in_inbound(inbound_id: Optional[int] = None)`

Resets traffic data for all clients in the specified inbound.

```python
await client.reset_all_clients_in_inbound(inbound_id=1234)
```

**Parameters:**
- `inbound_id` (`int`, optional): The ID of the inbound. Defaults to `None`.

---

#### Method  `delete_depleted_clients(inbound_id: Optional[int] = None)`

Deletes clients with expired keys in the specified inbound.

```python
await client.delete_depleted_clients(inbound_id=1234)
```

**Parameters:**
- `inbound_id` (`int`, optional): The ID of the inbound. Defaults to `None`.

---

#### Method  `get_clients_in_inbound(inbound_id: Optional[int] = None) -> list`

Retrieves a list of clients in the specified inbound.

```python
clients = await client.get_clients_in_inbound(inbound_id=1234)
```

**Parameters:**
- `inbound_id` (`int`, optional): The ID of the inbound. Defaults to `None`.

**Returns:**
- `list`: A list of clients in the specified inbound.

---

### Client Management

#### Method `get_client_traffic(email: str) -> PanelResponse`

Retrieves traffic data for a client by email.

```python
traffic = await client.get_client_traffic(email="client@example.com")
```

**Parameters:**
- `email` (`str`): The email of the client.

**Returns:**
- `PanelResponse`: Traffic data for the client.

---

#### Method `get_client_traffic_by_id(client_id: str) -> PanelResponse`

Retrieves traffic data for a client by ID.

```python
traffic = await client.get_client_traffic_by_id(client_id="client1234")
```

**Parameters:**
- `client_id` (`str`): The unique ID of the client.

**Returns:**
- `PanelResponse`: Traffic data for the client.

---

#### Method `add_client(payload: ClientPayload) -> str`

Adds a client to the specified inbound and returns a subscription link.

```python
link = await client.add_client(payload)
```

**Parameters:**
- `payload` (`ClientPayload`): The details of the client to add.

**Returns:**
- `str`: A subscription link for the new client.

---

#### Method `update_client(client_id: str, payload: ClientPayload) -> str`

Updates a client's details and returns a subscription link.

```python
link = await client.update_client(client_id="client1234", payload=updated_payload)
```

**Parameters:**
- `client_id` (`str`): The unique ID of the client.
- `payload` (`ClientPayload`): The updated details for the client.

**Returns:**
- `str`: A subscription link for the updated client.

---

#### Method `delete_client(client_id: str, inbound_id: Optional[int] = None)`

Deletes a client by ID.

```python
await client.delete_client(client_id="client1234")
```

**Parameters:**
- `client_id` (`str`): The unique ID of the client.
- `inbound_id` (`int`, optional): The ID of the inbound. Defaults to `None`.

---

#### Method `client_ipaddress(email: str) -> PanelResponse`

Retrieves a client's IP address.

```python
ip = await client.client_ipaddress(email="client@example.com")
```

**Parameters:**
- `email` (`str`): The email of the client.

**Returns:**
- `PanelResponse`: The client's IP address.

---

#### Method `clear_client_ipadresses(email: str)`

Clears a client's IP addresses.

```python
await client.clear_client_ipadresses(email="client@example.com")
```

**Parameters:**
- `email` (`str`): The email of the client.

---

#### Method `reset_client_traffic(email: str, inbound_id: Optional[int] = None)`

Resets a client's traffic data.

```python
await client.reset_client_traffic(email="client@example.com", inbound_id=1234)
```

**Parameters:**
- `email` (`str`): The email of the client.
- `inbound_id` (`int`, optional): The ID of the inbound. Defaults to `None`.

---

# PanelResponce

## Class: `PanelResponce`

A utility class for representing responses from the Panel API.

### Constructor

#### `__init__(response: dict)`

Initializes a `PanelResponse` object using the response dictionary from the Panel API.

**Parameters:**
- `response` (`dict`): The response dictionary from the Panel API. Expected keys include:
  - `success` (`bool`, optional): Indicates whether the operation was successful. Defaults to `False`.
  - `message` (`str`, optional): A message describing the result of the operation. Defaults to an empty string.
  - `obj` (`Any`, optional): Additional data or objects returned by the API. Defaults to `None`.

**Example:**
```python
response_data = {
    "success": True,
    "message": "Operation completed successfully.",
    "obj": {"key": "value"}
}
panel_response = PanelResponse(response_data)
```

---

### Attributes

- **`success`** (`bool`): Indicates whether the operation was successful.
- **`message`** (`str`): A descriptive message about the response.
- **`obj`** (`Any`): Additional data or objects returned by the API.

---

### Methods

#### `__repr__()`

Returns a string representation of the `PanelResponse` object.

**Example:**
```python
response_data = {
    "success": True,
    "message": "Operation completed successfully.",
    "obj": {"key": "value"}
}
panel_response = PanelResponse(response_data)
print(repr(panel_response))
```

**Output:**
```
PanelResponse object (
success : True
msg : Operation completed successfully.
obj : {'key': 'value'}
)
```

---

# Errors

## Class: `ClientError`

A custom exception class for handling client-related errors.

### Constructor

#### `__init__(text: str, status: int)`

Initializes a `ClientError` instance with an error message and status code.

**Parameters:**
- `text` (`str`): A description of the error.
- `status` (`int`): The status code associated with the error.

**Example:**
```python
try:
    raise ClientError("Invalid request", 400)
except ClientError as e:
    print(e)
```

---

### Attributes

- **`txt`** (`str`): The description of the error.
- **`status`** (`int`): The status code associated with the error.

---

### Methods

#### `__repr__()`

Returns a formatted string representation of the `ClientError` instance, including the error message and status code.

**Example:**
```python
error = ClientError("Unauthorized access", 401)
print(repr(error))

# ClientError:  Unauthorized access 
# status: [401]
```

---

