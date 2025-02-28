# python-openhab-rest-client

A Python client for the openHAB REST API. This library enables easy interaction with the openHAB REST API to control smart home devices, retrieve status information, and process events.

## Features

Supports the following openHAB REST API endpoints:

- Actions
- Addons
- Audio
- Auth
- ChannelTypes
- ConfigDescriptions
- Discovery
- Events (ItemEvents, ThingEvents, InboxEvents, LinkEvents, ChannelEvents)
- Iconsets
- Inbox
- Items
- Links
- Logging
- ModuleTypes
- Persistence
- ProfileTypes
- Rules
- Services
- Sitemaps
- Systeminfo
- Tags
- Templates
- ThingTypes
- Things
- Transformations
- UI
- UUID
- Voice

Supports both Server-Sent Events (SSE) and regular REST requests. SSE is used for the events of openHAB.

## Requirements

- Python 3.x
- `requests`
- `json`

## Installation

Install via pip:

```sh
pip install python-openhab-rest-client
```

## Usage

Basically, you always need the `OpenHABClient`. Regardless of whether you carry out a normal `REST request` or one via `SSE`.

### Authentication

#### Basic Authentication

```python
from openhab import OpenHABClient

client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
```

The `url`, the `username` and the `password` can also vary. In particular, it is possible that `url` could be a remote IP address or even the openHAB cloud.

#### Token-based Authentication

It is also conceivable that a `token` could be used instead of `basic authentication`, i.e. with a `username` and `password`. A `token` is used by default in openHAB. The `basic authentication` must actually be activated manually.

For token-based access, the initialization of the client is as follows:

```python
client = OpenHABClient(url="http://127.0.0.1:8080", token="oh.openhab.U0doM1Lz4kJ6tPlVGjH17jjm4ZcTHIHi7sMwESzrIybKbCGySmBMtysPnObQLuLf7PgqnI7jWQ5LosySY8Q")
```

Of course, your `token` will probably look different here too.

### Requests

#### Normal REST requests

Depending on the `endpoint`, a corresponding class must be imported from the library. If you want to access endpoints of the REST API with which you want to access `items`, you import the `Items` class, for example. There are then different functions in this class for each endpoint for items. More details can be found in the documentation.

An easy example could be:

```python
from openhab import OpenHABClient, Items

client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
itemsAPI = Items(client)

allItems = itemsAPI.getAllItems()
print("All Items:", allItems)
```

#### Server-sent Events (SSE) requests

All normal REST requests are static. This means that they do not react to status changes. You would therefore have to send several REST requests in succession (polling). Or you can use the various evetnts from openHAB. This can be done using server-sent events (SSE) without polling. The server sends a message to the client exactly when it can make something available. With polling, on the other hand, you would have to constantly send requests to the server, which would significantly increase the network and server load.

There are various [events](https://www.openhab.org/docs/developer/utils/events.html) in openHAB. For `ItemEvents`, `ThingEvents`, `InboxEvents`, `LinkEvents` and `ChannelEvents` there are own classes. However, there is also the `Events` class. More information can be found in the documentation.

An example looks like this:

```python
from openhab import OpenHABClient, ItemEvents

client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
itemEvents = ItemEvents(client)

response =  itemEvents.ItemStateChangedEvent()

with response as events:
    for line in events.iter_lines():
        line = line.decode()

        if "data" in line:
            line = line.replace("data: ", "")

            try:
                data = json.loads(line)
                print(data)
            except json.decoder.JSONDecodeError:
                print("Event could not be converted to JSON")
```

### Tests

There is also a test function for each function. This means that every class that you import also has a test class that you can import. These tests work with a try-catch, as well as with a print output. Neither the value of the REST API nor something like True or False is returned. Effectively, however, the actual function is called from this test function and also executed in full, unless an exception is thrown.

In other words... For example, if you use the following import,

```python
from openhab import Items
```

then the test class to be imported would be the following:

```python
from openhab.tests import ItemsTest
```

From e.g. the following function

```python

itemsAPI = Items(client)
itemsAPI.sendCommand("testSwitch", "ON")
```

then becomes the following function for the test:

```python

itemsTest = ItemsTest(client)
itemsTest.testSendCommand("testSwitch", "ON")
```

However, both would also really execute a sendCommand in openHAB. The test classes test whether a function can be executed. In the end, it can only not be executed if the endpoint does not exist or has been implemented incorrectly. However, a non-existent endpoint can also occur, for example, if the name of the item is incorrect.

## Full list of Methods

### OpenHABClient

`OpenHABClient` is a Python class that provides an interface to interact with the openHAB REST API. It allows users to send requests to openHAB to retrieve and manipulate smart home devices, events, and configurations. The get, put, post and delete methods are used in the other classes for the client. You therefore do not need to use them raw.

#### Initialization

##### Constructor

```python
from openhab import OpenHABClient

OpenHABClient(url: str, username: str = None, password: str = None, token: str = None)
```
###### Parameters:
- `url` (str): The base URL of the openHAB server (e.g., "http://127.0.0.1:8080").
- `username` (str, optional): Username for Basic Authentication (default is `None`).
- `password` (str, optional): Password for Basic Authentication (default is `None`).
- `token` (str, optional): Bearer Token for Token-based Authentication (default is `None`).

###### Example:

```python
client = OpenHABClient("http://127.0.0.1:8080", username="admin", password="password")
```

#### Methods

##### `get`

```python
get(endpoint: str, header: dict = None, params: dict = None)
```

Sends a GET request to the openHAB server.

###### Parameters:
- `endpoint` (str): The API endpoint (e.g., `"/items"`).
- `header` (dict, optional): Headers to include in the request.
- `params` (dict, optional): Query parameters for the request.

###### Example:

```python
response = client.get("/items")
print(response)
```

##### `post`

```python
post(endpoint: str, header: dict = None, data=None, params: dict = None)
```

Sends a POST request to the openHAB server.

###### Parameters:
- `endpoint` (str): The API endpoint (e.g., `"/items"`).
- `header` (dict, optional): Headers to include in the request.
- `data` (optional): Data to send in the request body.
- `params` (dict, optional): Query parameters for the request.

###### Example:

```python
data = {"type": "Switch", "state": "ON"}
response = client.post("/items/light", data=json.dumps(data))
print(response)
```

##### `put`

```python
put(endpoint: str, header: dict = None, data=None, params: dict = None)
```

Sends a PUT request to update a resource in openHAB.

###### Example:

```python
data = {"state": "OFF"}
response = client.put("/items/light", data=json.dumps(data))
print(response)
```

##### `delete`

```python
delete(endpoint: str, header: dict = None, data=None, params: dict = None)
```

Sends a DELETE request to remove a resource from openHAB.

###### Example:

```python
response = client.delete("/items/light")
print(response)
```

#### Authentication

The client supports two types of authentication:
- **Basic Authentication** (Username & Password)
- **Bearer Token Authentication**

If a token is provided, it is used for authentication; otherwise, Basic Authentication is used if credentials are supplied.

#### Error Handling

Errors during requests are caught and logged, with appropriate exception handling for HTTP errors, connection issues, and timeouts.


### Actions

The `Actions` class provides methods to interact with the OpenHAB actions API. It allows retrieving available actions for a specific `thingUID` and executing actions.

#### Initialization

```python
from openhab import OpenHABClient, Actions

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
actions = Actions(client)
```

#### Methods

##### `getAllActions(thingUID: str, language: str = None) -> list`

Retrieves all available actions for a given thing UID.

**Parameters:**
- `thingUID` (str): The UID of the thing for which actions should be retrieved.
- `language` (str, optional): The language for the response (sets the `Accept-Language` header).

**Returns:**
- `list`: A list of available actions.

###### Example:
```python
actions_list = actions.getAllActions("myThingUID")
print(actions_list)
```

##### `execute_action(thingUID: str, actionUID: str, actionInputs: dict, language: str = None) -> str`

Executes an action on a specific thing.

**Parameters:**
- `thingUID` (str): The UID of the thing on which the action is executed.
- `actionUID` (str): The UID of the action to be performed.
- `actionInputs` (dict): A dictionary containing input parameters for the action.
- `language` (str, optional): The language for the response (sets the `Accept-Language` header).

**Returns:**
- `str`: The response from the OpenHAB server.

###### Example:

```python
response = actions.execute_action("myThingUID", "actionID", {"param1": "value1"})
print(response)
```

### Addons

The `Addons` class provides methods for interacting with the openHAB add-ons via the REST API.

#### Methods

##### `getAddons(serviceID: str = None, language: str = None) -> dict`

Retrieves a list of all available add-ons.

**Parameters:**
- `serviceID` (optional): Filter by service ID.
- `language` (optional): Language preference for the response.

**Returns:**
A dictionary containing add-ons data.

##### `getAddon(addonID: str, serviceID: str = None, language: str = None) -> dict`

Retrieves details of a specific add-on by its ID.

**Parameters:**
- `addonID`: The unique identifier of the add-on.
- `serviceID` (optional): Filter by service ID.
- `language` (optional): Language preference for the response.

**Returns:**
A dictionary containing details of the specified add-on.

##### `getAddonConfig(addonID: str, serviceID: str = None) -> dict`

Retrieves the configuration of a specific add-on.

**Parameters:**
- `addonID`: The unique identifier of the add-on.
- `serviceID` (optional): Filter by service ID.

**Returns:**
A dictionary containing the configuration of the add-on.

##### `updateAddonConfig(addonID: str, configData: dict, serviceID: str = None) -> dict`

Updates the configuration of a specific add-on.

**Parameters:**
- `addonID`: The unique identifier of the add-on.
- `configData`: Dictionary containing new configuration settings.
- `serviceID` (optional): Specify the target service.

**Returns:**
A dictionary containing the updated configuration.

##### `installAddon(addonID: str, serviceID: str = None, language: str = None) -> dict`

Installs an add-on by its ID.

**Parameters:**
- `addonID`: The unique identifier of the add-on.
- `serviceID` (optional): Specify the target service.
- `language` (optional): Language preference for the response.

**Returns:**
A dictionary containing the installation status.

##### `uninstallAddon(addonID: str, serviceID: str = None, language: str = None) -> dict`

Uninstalls an add-on by its ID.

**Parameters:**
- `addonID`: The unique identifier of the add-on.
- `serviceID` (optional): Specify the target service.
- `language` (optional): Language preference for the response.

**Returns:**
A dictionary containing the uninstallation status.

##### `getAddonServices(language: str = None) -> dict`

Retrieves a list of all available add-on services.

**Parameters:**
- `language` (optional): Language preference for the response.

**Returns:**
A dictionary containing available add-on services.

##### `getAddonSuggestions(language: str = None) -> dict`

Retrieves a list of suggested add-ons for installation.

**Parameters:**
- `language` (optional): Language preference for the response.

**Returns:**
A dictionary containing suggested add-ons.

##### `getAddonTypes(language: str = None) -> dict`

Retrieves a list of all available add-on types.

**Parameters:**
- `language` (optional): Language preference for the response.

**Returns:**
A dictionary containing available add-on types.

##### `installAddonFromUrl(url: str) -> dict`

Installs an add-on from a given URL.

**Parameters:**
- `url`: The URL of the add-on to install.

**Returns:**
A dictionary containing the installation status.

### Audio

The `Audio` class provides methods for interacting with the OpenHAB audio API. It allows retrieving default audio sinks and sources, as well as listing available sinks and sources.

#### Initialization

```python
from openhab import OpenHABClient, Audio

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
audio = Audio(client)
```

#### Methods

##### `getDefaultSink(language: str = None) -> dict`

Retrieves the default audio sink if defined, or the first available sink.

**Parameters:**
- `language` (str, optional): The language for the response (sets the `Accept-Language` header).

**Returns:**
- `dict`: Information about the default sink.

###### Example:

```python
default_sink = audio.getDefaultSink()
print(default_sink)
```

##### `getDefaultSource(language: str = None) -> dict`

Retrieves the default audio source if defined, or the first available source.

**Parameters:**
- `language` (str, optional): The language for the response (sets the `Accept-Language` header).

**Returns:**
- `dict`: Information about the default source.

###### Example:

```python
default_source = audio.getDefaultSource()
print(default_source)
```

##### `getSinks(language: str = None) -> list`

Retrieves a list of all available audio sinks.

**Parameters:**
- `language` (str, optional): The language for the response (sets the `Accept-Language` header).

**Returns:**
- `list`: A list of available audio sinks.

###### Example:

```python
sinks = audio.getSinks()
print(sinks)
```

##### `getSources(language: str = None) -> list`

Retrieves a list of all available audio sources.

**Parameters:**
- `language` (str, optional): The language for the response (sets the `Accept-Language` header).

**Returns:**
- `list`: A list of available audio sources.

###### Example:

```python
sources = audio.getSources()
print(sources)
```

### Auth

The `Auth` class provides methods for handling authentication in OpenHAB, including retrieving API tokens, revoking tokens, logging out, and managing authentication sessions.

#### Initialization

```python
from openhab import OpenHABClient, Auth

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
auth = Auth(client)
```

#### Methods

##### `getAPITokens(language: str = None) -> dict`

Retrieves the API tokens associated with the authenticated user.

**Parameters:**
- `language` (str, optional): The language for the request (sets the `Accept-Language` header).

**Returns:**
- `dict`: JSON response containing API tokens.

###### Example:

```python
tokens = auth.getAPITokens()
print(tokens)
```

##### `revokeAPIToken(tokenName: str, language: str = None) -> dict`

Revokes a specific API token associated with the authenticated user.

**Parameters:**
- `tokenName` (str): The name of the API token to revoke.
- `language` (str, optional): The language for the request.

**Returns:**
- `dict`: JSON response confirming the revocation.

###### Example:

```python
response = auth.revokeAPIToken("my_token")
print(response)
```

##### `logout(refreshToken: str, language: str = None) -> dict`

Terminates the session associated with a given refresh token.

**Parameters:**
- `refreshToken` (str): The refresh token used to delete the session.
- `language` (str, optional): The language for the request.

**Returns:**
- `dict`: JSON response confirming the logout.

###### Example:

```python
response = auth.logout("my_refresh_token")
print(response)
```

##### `getSessions(language: str = None) -> dict`

Retrieves the sessions associated with the authenticated user.

**Parameters:**
- `language` (str, optional): The language for the request.

**Returns:**
- `dict`: JSON response containing session details.

###### Example:

```python
sessions = auth.getSessions()
print(sessions)
```

##### `getToken(grantType: str, code: str = None, redirectURI: str = None, clientID: str = None, refreshToken: str = None, codeVerifier: str = None, language: str = None) -> dict`

Obtains access and refresh tokens.

**Parameters:**
- `grantType` (str): The type of grant being requested.
- `code` (str, optional): Authorization code for authentication.
- `redirectURI` (str, optional): Redirect URI for OAuth authentication.
- `clientID` (str, optional): Client ID for authentication.
- `refreshToken` (str, optional): Refresh token for token renewal.
- `codeVerifier` (str, optional): Code verifier for PKCE authentication.
- `language` (str, optional): The language for the request.

**Returns:**
- `dict`: JSON response containing access and refresh tokens.

###### Example:

```python
token_response = auth.getToken(
    grantType="authorization_code",
    code="auth_code",
    redirectURI="http://localhost/callback",
    clientID="client123",
    codeVerifier="verifier123"
)
print(token_response)
```

### ChannelTypes

The `ChannelTypes` class provides methods to interact with OpenHAB's channel types, allowing retrieval of all available channel types, specific channel types by UID, and linkable item types.

#### Initialization

```python
from openhab import OpenHABClient, ChannelTypes

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
channelTypes = ChannelTypes(client)
```

#### Methods

##### `getAllChannelTypes(language: str = None, prefixes: str = None) -> list`

Retrieves all available channel types.

**Parameters:**
- `language` (str, optional): The preferred language for the response (`Accept-Language` header).
- `prefixes` (str, optional): A query parameter to filter channel types by prefix.

**Returns:**
- `list`: A list of available channel types.

###### Example:

```python
channels = channel_types.getAllChannelTypes(language="en", prefixes="zwave")
print(channels)
```

##### `getChannelTypeByUID(channelTypeUID: str, language: str = None) -> dict`

Retrieves details of a specific channel type by its UID.

**Parameters:**
- `channelTypeUID` (str): The unique identifier of the channel type.
- `language` (str, optional): The preferred language for the response.

**Returns:**
- `dict`: JSON response containing details of the specified channel type.

###### Example:

```python
channelDetails = channelTypes.getChannelTypeByUID("zwave:switch_binary", language="en")
print(channelDetails)
```

##### `getLinkableItemTypes(channelTypeUID: str) -> list`

Retrieves the item types that can be linked to a specified trigger channel type.

**Parameters:**
- `channelTypeUID` (str): The unique identifier of the channel type.

**Returns:**
- `list`: A list of item types that can be linked to the given channel type.

###### Example:

```python
linkableItems = channelTypes.getLinkableItemTypes("zwave:switch_binary")
print(linkableItems)
```

### ConfigDescriptions

The `ConfigDescriptions` class provides methods to interact with OpenHAB's configuration descriptions, allowing retrieval of all available descriptions and specific descriptions by URI.

#### Initialization

```python
from openhab import OpenHABClient, ConfigDescriptions

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
configDescriptions = ConfigDescriptions(client)
```

#### Methods

##### `getAllConfigDescriptions(language: str = None, scheme: str = None) -> list`

Retrieves all available configuration descriptions.

**Parameters:**
- `language` (str, optional): The preferred language for the response (`Accept-Language` header).
- `scheme` (str, optional): A query parameter to filter results by a specific scheme.

**Returns:**
- `list`: A list of available configuration descriptions.

###### Example:

```python
configs = configDescriptions.getAllConfigDescriptions(language="en", scheme="thing")
print(configs)
```

##### `getConfigDescriptionByUri(uri: str, language: str = None) -> dict`

Retrieves a specific configuration description by its URI.

**Parameters:**
- `uri` (str): The URI of the requested configuration description.
- `language` (str, optional): The preferred language for the response.

**Returns:**
- `dict`: JSON response containing details of the specified configuration description.

###### Example:

```python
configDetails = configDescriptions.getConfigDescriptionByURI("thing-type:zwave:device", language="en")
print(config_details)
```

### Discovery

The `Discovery` class provides methods to interact with OpenHAB's discovery service, allowing retrieval of all available bindings that support discovery and starting a discovery scan for specific bindings.

#### Initialization

```python
from openhab import OpenHABClient, Discovery

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
discovery = Discovery(client)
```

#### Methods

##### `getAllDiscoveryBindings() -> list`

Retrieves all bindings that support discovery.

**Returns:**
- `list`: A list of strings representing the bindings that support discovery.

###### Example:

```python
bindings = discovery.getAllDiscoveryBindings()
print(bindings)
```

##### `startBindingScan(bindingID: str) -> int`
Starts the asynchronous discovery process for a binding and returns the timeout duration in seconds.

**Parameters:**
- `bindingID` (str): The ID of the binding for which the discovery process is to be started.

**Returns:**
- `int`: Timeout duration of the discovery operation in seconds.

###### Example:

```python
timeout = discovery.startBindingScan("zwave")
print(timeout)
``` 

### Events

The `Events` class provides methods to interact with OpenHAB's event service. It allows you to retrieve various event streams, including item-related events, thing-related events, inbox events, and more.

#### Initialization

```python
from openhab import OpenHABClient, Events

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
events = Events(client)
```

#### Methods

##### `getAllEvents(topics: str = None) -> list`

Retrieves all available events, optionally filtered by topic.

**Parameters:**
- `topics` (str, optional): A comma-separated list of topics to filter the events by.

**Returns:**
- `list`: A SSE stream of events.

###### Example:

```python
events = events.getAllEvents(topics="openhab/items")
print(events)
```

##### `initiateStateTracker() -> str`

Initiates a new item state tracker connection.

**Returns:**
- `str`: The connection ID as a string.

###### Example:

```python
connectionID = events.initiateStateTracker()
print(connectionID)
```

##### `updateSSEConnectionItems(connectionID: str, items: list) -> str`

Changes the list of items an SSE connection will receive state updates for.

**Parameters:**
- `connectionID` (str): The ID of the existing connection.
- `items` (list): A list of item names to subscribe to for state updates.

**Returns:**
- `str`: A success message when the update is completed.

###### Example:

```python
successMessage = events.updateSSEConnectionItems(connectionID, ["item1", "item2"])
print(successMessage)
```

#### `ItemEvents` Class

The `ItemEvents` class allows you to retrieve events related to items.

##### `ItemEvent()`

Get all item-related events.

**Returns:**
- `list`: A SSE stream of item events.

##### `ItemAddedEvent(itemName: str = "*")`

Get events for added items.

**Parameters:**
- `itemName` (str, optional): The name of the item (default is "*").

**Returns:**
- `list`: A SSE stream of added item events.

##### `ItemRemovedEvent(itemName: str = "*")`

Get events for removed items.

**Parameters:**
- `itemName` (str, optional): The name of the item (default is "*").

**Returns:**
- `list`: A SSE stream of removed item events.

##### `ItemUpdatedEvent(itemName: str = "*")`

Get events for updated items.

**Parameters:**
- `itemName` (str, optional): The name of the item (default is "*").

**Returns:**
- `list`: A SSE stream of updated item events.

##### `ItemCommandEvent(itemName: str = "*")`

Get events for item commands.

**Parameters:**
- `itemName` (str, optional): The name of the item (default is "*").

**Returns:**
- `list`: A SSE stream of item command events.

##### `ItemStateEvent(itemName: str = "*")`

Get events for item state changes.

**Parameters:**
- `itemName` (str, optional): The name of the item (default is "*").

**Returns:**
- `list`: A SSE stream of item state events.

##### `ItemStatePredictedEvent(itemName: str = "*")`

Get events for predicted item state changes.

**Parameters:**
- `itemName` (str, optional): The name of the item (default is "*").

**Returns:**
- `list`: A SSE stream of predicted item state events.

##### `ItemStateChangedEvent(itemName: str = "*")`

Get events for item state changes.

**Parameters:**
- `itemName` (str, optional): The name of the item (default is "*").

**Returns:**
- `list`: A SSE stream of state changed events.

#### `ThingEvents` Class

The `ThingEvents` class allows you to retrieve events related to things.

##### `ThingAddedEvent(thingUID: str = "*")`

Get events for added things.

**Parameters:**
- `thingUID` (str, optional): The UID of the thing (default is "*").

**Returns:**
- `list`: A SSE stream of added thing events.

##### `ThingRemovedEvent(thingUID: str = "*")`

Get events for removed things.

**Parameters:**
- `thingUID` (str, optional): The UID of the thing (default is "*").

**Returns:**
- `list`: A SSE stream of removed thing events.

##### `ThingUpdatedEvent(thingUID: str = "*")`

Get events for updated things.

**Parameters:**
- `thingUID` (str, optional): The UID of the thing (default is "*").

**Returns:**
- `list`: A SSE stream of updated thing events.

##### `ThingStatusInfoEvent(thingUID: str = "*")`

Get events for thing status information.

**Parameters:**
- `thingUID` (str, optional): The UID of the thing (default is "*").

**Returns:**
- `list`: A SSE stream of status information events.

##### `ThingStatusInfoChangedEvent(thingUID: str = "*")`

Get events for thing status information changes.

**Parameters:**
- `thingUID` (str, optional): The UID of the thing (default is "*").

**Returns:**
- `list`: A SSE stream of status changed events.

#### `InboxEvents` Class

The `InboxEvents` class allows you to retrieve events related to things in the inbox.

##### `InboxAddedEvent(thingUID: str = "*")`

Get events for added things in the inbox.

**Parameters:**
- `thingUID` (str, optional): The UID of the thing (default is "*").

**Returns:**
- `list`: A SSE stream of added inbox events.

##### `InboxRemovedEvent(thingUID: str = "*")`

Get events for removed things in the inbox.

**Parameters:**
- `thingUID` (str, optional): The UID of the thing (default is "*").

**Returns:**
- `list`: A SSE stream of removed inbox events.

##### `InboxUpdatedEvent(thingUID: str = "*")`

Get events for updated things in the inbox.

**Parameters:**
- `thingUID` (str, optional): The UID of the thing (default is "*").

**Returns:**
- `list`: A SSE stream of updated inbox events.

#### `LinkEvents` Class

The `LinkEvents` class allows you to retrieve events related to item-channel links.

##### `ItemChannelLinkAddedEvent(itemName: str = "*", channelUID: str = "*")`

Get events for added item-channel links.

**Parameters:**
- `itemName` (str, optional): The name of the item (default is "*").
- `channelUID` (str, optional): The UID of the channel (default is "*").

**Returns:**
- `list`: A SSE stream of added item-channel link events.

##### `ItemChannelLinkRemovedEvent(itemName: str = "*", channelUID: str = "*")`

Get events for removed item-channel links.

**Parameters:**
- `itemName` (str, optional): The name of the item (default is "*").
- `channelUID` (str, optional): The UID of the channel (default is "*").

**Returns:**
- `list`: A SSE stream of removed item-channel link events.

#### `ChannelEvents` Class

The `ChannelEvents` class allows you to retrieve events related to channel descriptions and triggers.

##### `ChannelDescriptionChangedEvent(channelUID: str = "*")`

Get events for changes in channel descriptions.

**Parameters:**
- `channelUID` (str, optional): The UID of the channel (default is "*").

**Returns:**
- `list`: A SSE stream of channel description changed events.

##### `ChannelTriggeredEvent(channelUID: str = "*")`

Get events for triggered channels.

**Parameters:**
- `channelUID` (str, optional): The UID of the channel (default is "*").

**Returns:**
- `list`: A SSE stream of triggered channel events.

### Iconsets

The `Iconsets` class provides methods to interact with OpenHAB's icon sets. It allows you to retrieve all available icon sets, optionally filtered by language.

#### Initialization

```python
from openhab import OpenHABClient, Iconsets

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
iconsets = Iconsets(client)
```

#### Methods

##### `getAllIconsets(language: str = None) -> list`

Gets all icon sets, optionally filtered by language.

**Parameters:**
- `language` (str, optional): An optional language preference for the response (e.g., 'en', 'de').

**Returns:**
- `list`: A list of icon sets with details such as ID, label, description, and supported formats.

###### Example:

```python
iconsets = iconsets.getAllIconsets(language="en")
print(iconsets)
```

### Inbox

The `Inbox` class provides methods to interact with the inbox of discovered things in OpenHAB. It allows you to retrieve all discovered things, approve or ignore discovery results, and remove entries from the inbox.

#### Initialization

```python
from openhab import OpenHABClient, Inbox

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
inbox = Inbox(client)
```

#### Methods

##### `getAllDiscoveredThings(includeIgnored: bool = True) -> list`

Gets all discovered things, optionally including ignored ones.

**Parameters:**
- `includeIgnored` (bool, optional): Whether ignored entries should also be included. Defaults to `True`.

**Returns:**
- `list`: A list of discovered things with details such as UID, flag, label, and properties.

###### Example:

```python
discoveredThings = inbox.getAllDiscoveredThings()
print(discoveredThings)
```

##### `removeDiscoveryResult(thingUID: str) -> dict`

Removes a discovery result from the inbox.

**Parameters:**
- `thingUID` (str): The UID of the discovered thing to be removed.

**Returns:**
- `dict`: The API response to the delete request.

###### Example:

```python
response = inbox.removeDiscoveryResult("someThingUID")
print(response)
```

##### `approveDiscoveryResult(thingUID: str, thingLabel: str, newThingID: str = None, language: str = None) -> dict`

Approves the discovery result by adding the thing to the registry.

**Parameters:**
- `thingUID` (str): The UID of the discovered thing.
- `thingLabel` (str): The new name of the thing.
- `newThingID` (str, optional): The new thing ID.
- `language` (str, optional): The language preference for the response.

**Returns:**
- `dict`: The API response to the approval request.

###### Example:
```python
response = inbox.approveDiscoveryResult("someThingUID", "NewThingLabel")
print(response)
```

##### `ignoreDiscoveryResult(thingUID: str) -> dict`

Flags a discovery result as ignored for further processing.

**Parameters:**
- `thingUID` (str): The UID of the discovered thing.

**Returns:**
- `dict`: The API response to the ignore request.

###### Example:

```python
response = inbox.ignoreDiscoveryResult("someThingUID")
print(response)
```

##### `unignoreDiscoveryResult(thingUID: str) -> dict`

Removes the ignore flag from a discovery result.

**Parameters:**
- `thingUID` (str): The UID of the discovered thing.

**Returns:**
- `dict`: The API response to the unignore request.

###### Example:

```python
response = inbox.unignoreDiscoveryResult("someThingUID")
print(response)
```

### Items

The `Items` class provides methods for managing OpenHAB items via the REST API. It enables the retrieval, addition, updating and deletion of items as well as the management of tags, metadata and statuses.

#### **Initilization**

```python
from openhab import OpenHABClient, Items

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
items = Items(client)
```

#### **Methoden**

##### `getAllItems(...) -> list`

Retrieves all available items.

**Parameter:**
- `language` (str, optional): Language filter for the header `Accept-Language`.
- `type` (str, optional): Item type filter.
- `tags` (str, optional): Item tag filter.
- `metadata` (str, optional): Metadata selector (default: `.*`).
- `recursive` (bool, optional): Should group members be retrieved recursively? (Default: `False`).
- `fields` (str, optional): Limitation to certain fields (comma-separated).
- `staticDataOnly` (bool, optional): Only return cached data? (Default: `False`).

**Example:**

```python
allItems = items.getAllItems(language="de", type="Switch")
print(allItems)
```

##### `addOrUpdateItems(items: list) -> dict`

Adds a list of items or updates existing ones.

**Parameter:**
- `items` (list): List of items as a dictionary.

**Example:**

```python
new_items = [{"name": "NewLight", "type": "Switch"}]
response = items.addOrUpdateItems(new_items)
print(response)
```

##### `getItem(itemName: str, ...) -> dict`

Gets the details of a single item.

**Parameter:**
- `itemName` (str): Name of the item.
- `language`, `metadata`, `recursive` (see `getAllItems`).

**Example:**

```python
itemData = items.getItem("LivingRoomLight")
print(itemData)
```

##### `addOrUpdateItem(itemName: str, itemData: dict, ...) -> dict`

Adds or updates an item.

**Parameter:**
- `itemName` (str): Name of the item.
- `itemData` (dict): Data of the item.
- `language` (str, optional).

**Example:**

```python
newItem = {"type": "Switch", "label": "New Light"}
response = items.addOrUpdateItem("NewLight", newItem)
print(response)
```

##### `sendCommand(itemName: str, command: str) -> dict`

Sends a command to an item.

**Example:**

```python
response = items.sendCommand("LivingRoomLight", "ON")
print(response)
```

##### `postUpdate(itemName: str, state: str) -> dict`

Updates the status of an item.

**Example:**

```python
response = items.postUpdate("LivingRoomLight", "OFF")
print(response)
```

##### `deleteItem(itemName: str) -> dict`

Deletes an item from the registry.

**Example:**

```python
response = items.deleteItem("OldItem")
print(response)
```

##### `addGroupMember(itemName: str, memberItemName: str) -> dict`

Adds an item to a group.

**Example:**

```python
response = items.addGroupMember("LivingRoomGroup", "NewLight")
print(response)
```

##### `removeGroupMember(itemName: str, memberItemName: str) -> dict`

Removes an item from a group.

**Example:**
```python
response = items.removeGroupMember("LivingRoomGroup", "OldLight")
print(response)
```

##### `addMetadata(itemName: str, namespace: str, metadata: dict) -> dict`

Adds metadata to an item.

**Example:**

```python
metadata = {"value": "20", "config": {"unit": "°C"}}
response = items.addMetadata("Thermostat", "temperature", metadata)
print(response)
```

##### `removeMetadata(itemName: str, namespace: str) -> dict`

Removes metadata from an item.

**Example:**

```python
response = items.removeMetadata("Thermostat", "temperature")
print(response)
```

##### `getMetadataNamespaces(itemName: str, ...) -> list`

Returns the metadata namespace of an item.

**Example:**

```python
namespaces = items.getMetadataNamespaces("Thermostat")
print(namespaces)
```

##### `getSemanticItem(itemName: str, semanticClass: str, ...) -> dict`

Returns the item of a specific semantic class.

**Example:**

```python
semanticItem = items.getSemanticItem("Thermostat", "Point")
print(semanticItem)
```

##### `getItemState(itemName: str) -> dict`

Gets the current status of an item.

**Example:**

```python
state = items.getItemState("LivingRoomLight")
print(state)
```

##### `updateItemState(itemName: str, state: str, ...) -> dict`

Updates the status of an item.

**Example:**

```python
response = items.updateItemState("LivingRoomLight", "ON")
print(response)
```

##### `addTag(itemName: str, tag: str) -> dict`

Adds a tag to an item.

**Example:**
```python
response = items.addTag("LivingRoomLight", "Lighting")
print(response)
```

##### `removeTag(itemName: str, tag: str) -> dict`

Removes a tag from an item.

**Example:**

```python
response = items.removeTag("LivingRoomLight", "Lighting")
print(response)
```

##### `purgeOrphanedMetadata() -> dict`

Deletes unused metadata.

**Example:**

```python
response = items.purgeOrphanedMetadata()
print(response)
```

### Links

The `Links` class provides methods to manage links between items and channels in OpenHAB via the REST API.

#### Methods

##### `getAllLinks(channelUID: str = None, itemName: str = None) -> list`

Retrieves all available links.

- `channelUID` *(optional, str)* – Filters by the Channel UID.  
- `itemName` *(optional, str)* – Filters by the Item Name.  

**Returns:** A list of links containing details such as `itemName`, `channelUID`, and configuration.  

##### `getIndividualLink(itemName: str, channelUID: str) -> dict`

Retrieves a specific link between an item and a channel.

- `itemName` *(str)* – The name of the item.  
- `channelUID` *(str)* – The UID of the channel.  

**Returns:** A dictionary containing details of the link, including the item, channel UID, and configuration.  

##### `linkItemToChannel(itemName: str, channelUID: str, configuration: dict) -> dict`

Creates a link between an item and a channel.

- `itemName` *(str)* – The name of the item.  
- `channelUID` *(str)* – The UID of the channel.  
- `configuration` *(dict)* – The configuration parameters for the link.  

**Returns:** The API response confirming the link creation.  

##### `unlinkItemFromChannel(itemName: str, channelUID: str) -> dict`

Removes a link between an item and a channel.

- `itemName` *(str)* – The name of the item.  
- `channelUID` *(str)* – The UID of the channel.  

**Returns:** The API response confirming the link removal.  

##### `deleteAllLinks(object: str) -> dict`

Deletes all links that refer to a specific item or thing.

- `object` *(str)* – The name of the item or the UID of the thing.  

**Returns:** The API response confirming the deletion.  

##### `getOrphanLinks() -> list`

Retrieves orphaned links, which refer to items connected to non-existent or broken channels.

**Returns:** A list of orphaned links.

##### `purgeUnusedLinks() -> dict`

Removes all unused or orphaned links.

**Returns:** The API response confirming the removal.  

### Logging

The `Logging` class provides methods to manage loggers in OpenHAB via the REST API.

#### Methods

##### `getAllLoggers() -> dict`

Retrieves all available loggers.

**Returns:** A dictionary containing all loggers with their names and logging levels.  

##### `getSingleLogger(loggerName: str) -> dict`

Retrieves a specific logger.

- `loggerName` *(str)* – The name of the logger.  

**Returns:** A dictionary containing the logger name and its current logging level.  

##### `modifyOrAddLogger(loggerName: str, level: str) -> dict`

Modifies an existing logger or creates a new one with a specified logging level.

- `loggerName` *(str)* – The name of the logger.  
- `level` *(str)* – The logging level (e.g., `DEBUG`, `INFO`, `WARN`, `ERROR`).  

**Returns:** The API response confirming the modification or addition.  

##### `removeLogger(loggerName: str) -> dict`

Removes a specific logger.

- `loggerName` *(str)* – The name of the logger.  

**Returns:** The API response confirming the removal.  

### ModuleTypes

The `ModuleTypes` class provides methods to retrieve module types in OpenHAB via the REST API.

#### Methods

##### `getModuleTypes(tags=None, typeFilter=None, language: str = None) -> list`

Retrieves all available module types.

- `tags` *(Optional, str)* – Filter for specific tags.  
- `typeFilter` *(Optional, str)* – Filter by module type (`action`, `condition`, `trigger`).  
- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.  

**Returns:** A list of available module types.

##### `getModuleType(moduleTypeUID: str, language: str = None) -> dict`

Retrieves a specific module type based on its UID.

- `moduleTypeUID` *(str)* – The UID of the module type.  
- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.  

**Returns:** A dictionary containing the module type information.  

### Persistence

The `Persistence` class provides methods to interact with OpenHAB's persistence services via the REST API.

#### Methods

##### `getAllServices() -> dict`

Retrieves a list of available persistence services.

**Returns:** A list of persistence services with their IDs, labels, and types.  

##### `getServiceConfiguration(serviceID: str) -> dict`

Retrieves the configuration of a specific persistence service.

- `serviceID` *(str)* – The ID of the persistence service.  

**Returns:** A dictionary containing the service configuration.  

##### `setServiceConfiguration(serviceID: str, config: dict) -> dict`

Sets the configuration of a persistence service.

- `serviceID` *(str)* – The ID of the persistence service.  
- `config` *(dict)* – The configuration data for the service.  

**Returns:** The API response after modifying the configuration.  

##### `deleteServiceConfiguration(serviceID: str) -> dict`

Deletes the configuration of a persistence service.

- `serviceID` *(str)* – The ID of the persistence service.  

**Returns:** The API response after deleting the configuration.  

##### `getItemsForService(serviceID: str) -> dict`

Retrieves a list of items available in a specific persistence service.

- `serviceID` *(str)* – The ID of the persistence service.  

**Returns:** A list of items with their last and earliest timestamps.  

##### `getItemPersistenceData(serviceID: str, itemName: str, startTime: str = None, endTime: str = None, page: int = 1, pageLength: int = 50) -> dict`

Retrieves persistence data for a specific item from a persistence service.

- `serviceID` *(str)* – The ID of the persistence service.  
- `itemName` *(str)* – The name of the item.  
- `startTime` *(Optional, str)* – The start time for the data. Defaults to one day before `endTime`.  
- `endTime` *(Optional, str)* – The end time for the data. Defaults to the current time.  
- `page` *(Optional, int)* – The page number for paginated results. Defaults to `1`.  
- `pageLength` *(Optional, int)* – The number of data points per page. Defaults to `50`.  

**Returns:** The retrieved data points of the item.  

##### `storeItemData(serviceID: str, itemName: str, time: str, state: str) -> dict`

Stores persistence data for a specific item.

- `serviceID` *(str)* – The ID of the persistence service.  
- `itemName` *(str)* – The name of the item.  
- `time` *(str)* – The timestamp for the stored data.  
- `state` *(str)* – The state value to be stored.  

**Returns:** The API response after storing the data.  

##### `deleteItemData(serviceID: str, itemName: str, startTime: str, endTime: str) -> dict`

Deletes persistence data for a specific item within a given time range.

- `serviceID` *(str)* – The ID of the persistence service.  
- `itemName` *(str)* – The name of the item.  
- `startTime` *(str)* – The start time of the data to be deleted.  
- `endTime` *(str)* – The end time of the data to be deleted.  

**Returns:** The API response after deleting the data.  

### ProfileTypes

The `ProfileTypes` class provides methods to interact with OpenHAB's profile types via the REST API.

#### Methods

##### `getProfileTypes(channelTypeUID: str = None, itemType: str = None, language: str = None) -> dict`

Retrieves all available profile types.

- `channelTypeUID` *(Optional, str)* – Filters the results by channel type UID.  
- `itemType` *(Optional, str)* – Filters the results by item type.  
- `language` *(Optional, str)* – Specifies the language for the `Accept-Language` header.  

**Returns:** A list of profile types.  

### Rules

The `Rules` class provides methods to interact with OpenHAB's rules via the REST API.

#### Methods

##### `getRules(prefix: str = None, tags: list = None, summary: bool = False, staticDataOnly: bool = False) -> dict`

Retrieves available rules, optionally filtered by tags and/or prefix.

- `prefix` *(Optional, str)* – Filters results by prefix.  
- `tags` *(Optional, list)* – Filters results by tag array.  
- `summary` *(Optional, bool)* – If `True`, only summary fields are returned.  
- `staticDataOnly` *(Optional, bool)* – If `True`, only static data is returned.  

**Returns:** A list of rules (JSON objects).  

##### `createRule(ruleData: dict) -> dict`

Creates a new rule.

- `ruleData` *(dict)* – The rule data to be created.  

**Returns:** The created rule (JSON).  

##### `getRule(ruleUID: str) -> dict`

Retrieves a rule by its UID.

- `ruleUID` *(str)* – The UID of the rule.  

**Returns:** The rule object (JSON).  

##### `updateRule(ruleUID: str, ruleData: dict) -> dict`

Updates an existing rule.

- `ruleUID` *(str)* – The UID of the rule.  
- `ruleData` *(dict)* – The new rule data.  

**Returns:** The updated rule (JSON).  

##### `deleteRule(ruleUID: str) -> dict`

Removes a rule.

- `ruleUID` *(str)* – The UID of the rule.  

**Returns:** API response (status code).  

##### `setRuleState(ruleUID: str, enable: bool) -> dict`

Activates or deactivates a rule.

- `ruleUID` *(str)* – The UID of the rule.  
- `enable` *(bool)* – `True` to enable, `False` to disable.  

**Returns:** API response (status code).  

##### `enableRule(ruleUID: str) -> dict`

Enables a rule.  

##### `disableRule(ruleUID: str) -> dict`

Disables a rule. 

##### `runNow(ruleUID: str, contextData: dict = None) -> dict`

Executes the rule's actions immediately.

- `ruleUID` *(str)* – The UID of the rule.  
- `contextData` *(Optional, dict)* – Context data for execution.  

**Returns:** API response (status code).  

##### `simulateSchedule(fromTime: str, untilTime: str) -> dict`

Simulates rule executions filtered by the `Schedule` tag within a given timeframe.

- `fromTime` *(str)* – Start time of the simulation.  
- `untilTime` *(str)* – End time of the simulation.  

**Returns:** Simulation results (JSON).  

### Services

The `Services` class provides methods to interact with OpenHAB's configurable services via the REST API.

#### Methods

##### `getServices(language: str = None) -> dict`
Retrieves all configurable services.

- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.  

**Returns:** A list of services (JSON).  

##### `getService(serviceID: str, language: str = None) -> dict`

Retrieves a specific configurable service by its ID.

- `serviceID` *(str)* – The ID of the service.  
- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.  

**Returns:** The service object (JSON).  

##### `getServiceConfig(serviceID: str) -> dict`

Retrieves the configuration of a given service.

- `serviceID` *(str)* – The ID of the service.  

**Returns:** The configuration of the service (JSON).  

##### `updateServiceConfig(serviceID: str, configData: dict) -> dict`

Updates the configuration of a service and returns the old configuration.

- `serviceID` *(str)* – The ID of the service.  
- `configData` *(dict)* – The new configuration data.  

**Returns:** The old configuration of the service (JSON).  

##### `deleteServiceConfig(serviceID: str) -> dict`

Deletes the configuration of a given service and returns the old configuration.

- `serviceID` *(str)* – The ID of the service.  

**Returns:** The old configuration of the service (JSON).  

##### `getServiceContexts(serviceID: str, language: str = None) -> dict`

Retrieves multiple context service configurations for a given factory PID.

- `serviceID` *(str)* – The ID of the service.  
- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.  

**Returns:** A list of contexts (JSON).  

### Sitemaps

The `Sitemaps` class provides methods to interact with OpenHAB's sitemaps via the REST API.

#### Methods

##### `getSitemaps() -> dict`

Retrieves all available sitemaps.

**Returns:** A list of sitemaps (JSON).  

##### `getSitemap(sitemapName: str, language: str = None, type: str = None, jsonCallback: str = None, includeHidden: bool = False) -> dict`

Retrieves a specific sitemap by name.

- `sitemapName` *(str)* – The name of the sitemap.  
- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.  
- `type` *(Optional, str)* – Query parameter for type.  
- `jsonCallback` *(Optional, str)* – Query parameter for JSON callback.  
- `includeHidden` *(Optional, bool, default=False)* – Whether hidden widgets should be included.  

**Returns:** The sitemap object (JSON).

##### `getSitemapPage(sitemapName: str, pageID: str, subscriptionID: str = None, includeHidden: bool = False) -> dict`

Retrieves the data for a specific page within a sitemap.

- `sitemapName` *(str)* – The name of the sitemap.  
- `pageID` *(str)* – The ID of the page.  
- `subscriptionID` *(Optional, str)* – Query parameter for the subscription ID.  
- `includeHidden` *(Optional, bool, default=False)* – Whether hidden widgets should be included.  

**Returns:** The sitemap page (JSON).  

##### `getFullSitemap(sitemapName: str, subscriptionID: str = None, includeHidden: bool = False) -> dict`

Retrieves data for an entire sitemap.  
⚠ **Not recommended due to potentially high traffic.**

- `sitemapName` *(str)* – The name of the sitemap.  
- `subscriptionID` *(Optional, str)* – Query parameter for the subscription ID.  
- `includeHidden` *(Optional, bool, default=False)* – Whether hidden widgets should be included.  

**Returns:** The complete sitemap (JSON).  

##### `getSitemapEvents(subscriptionID: str, sitemap: str = None, pageID: str = None) -> dict`

Retrieves events for a specific sitemap or page.

- `subscriptionID` *(str)* – The ID of the subscription.  
- `sitemap` *(Optional, str)* – The name of the sitemap.  
- `pageID` *(Optional, str)* – The ID of the page.  

**Returns:** The events (JSON).  

##### `getFullSitemapEvents(subscriptionID: str, sitemap: str = None) -> dict`

Retrieves events for an entire sitemap.  
⚠ **Not recommended due to potentially high traffic.**

- `subscriptionID` *(str)* – The ID of the subscription.  
- `sitemap` *(Optional, str)* – The name of the sitemap.  

**Returns:** The events for the entire sitemap (JSON).  

##### `subscribeToSitemapEvents() -> dict`

Creates a sitemap event subscription.

**Returns:** The response to the subscription request (JSON).  

### Systeminfo

The `Systeminfo` class provides methods to retrieve system information via the OpenHAB REST API.

#### Methods

##### `getSystemInfo(language: str = None) -> dict`

Retrieves general system information.

- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.

**Returns:** A dictionary containing system information (JSON).

##### `getUoMInfo(language: str = None) -> dict`

Retrieves all supported units of measurement (UoM) and their system units.

- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.

**Returns:** A dictionary containing UoM information (JSON).

### Tags

The `Tags` class provides methods to manage semantic tags via the OpenHAB REST API.

#### Methods

##### `getTags(language: str = None) -> dict`

Retrieves all available semantic tags.

- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.

**Returns:** A list of semantic tags (JSON).

##### `createTag(tagData: dict, language: str = None) -> dict`

Creates a new semantic tag and adds it to the registry.

- `tagData` *(dict)* – The data object for the tag to be created.
- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.

**Returns:** The response to the tag creation request (JSON).

##### `getTag(tagID: str, language: str = None) -> dict`

Retrieves a semantic tag and its sub-tags.

- `tagID` *(str)* – The ID of the tag to retrieve.
- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.

**Returns:** The tag object and its sub-tags (JSON).

##### `updateTag(tagID: str, tagData: dict, language: str = None) -> dict`

Updates a semantic tag.

- `tagID` *(str)* – The ID of the tag to be updated.
- `tagData` *(dict)* – The new tag data.
- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.

**Returns:** The response to the tag update request (JSON).

##### `deleteTag(tagID: str, language: str = None) -> dict`
Removes a semantic tag and its sub-tags from the registry.

- `tagID` *(str)* – The ID of the tag to be removed.
- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.

**Returns:** The response to the tag deletion request (JSON).

### Templates

The `Templates` class provides methods to manage templates via the OpenHAB REST API.

#### Methods

##### `getAllTemplates(language: str = None) -> list`

Retrieves all available templates.

- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.

**Returns:** A list of templates (JSON).

##### `getTemplateByUID(templateUID: str, language: str = None) -> dict`

Retrieves a template corresponding to the given UID.

- `templateUID` *(str)* – The UID of the template.
- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.

**Returns:** A dictionary with the details of the template (JSON).

### ThingTypes

The `ThingTypes` class provides methods to retrieve available thing types via the OpenHAB REST API.

#### Methods

##### `getAllThingTypes(bindingID: str = None, language: str = None) -> list`

Retrieves all available thing types without configuration descriptions, channels, and properties.

- `bindingID` *(Optional, str)* – Filter the results by a specific binding ID.
- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.

**Returns:** A list of thing types (JSON).

##### `getThingType(thingTypeUID: str, language: str = None) -> dict`

Retrieves a thing type by its UID.

- `thingTypeUID` *(str)* – The UID of the thing type.
- `language` *(Optional, str)* – Language setting for the `Accept-Language` header.

**Returns:**  
A dictionary with the details of the thing type (JSON).  
If the thing type does not exist, an empty response with status **204** is returned.

### Things

The `Things` class provides methods to interact with available things in the OpenHAB system via the REST API.

#### Methods

##### `getAllThings(summary: bool = False, staticDataOnly: bool = False, language: str = None)`

Retrieves all available things.

- `summary` *(Optional, bool)* – If `True`, returns only the summary fields.
- `staticDataOnly` *(Optional, bool)* – If `True`, returns a cacheable list.
- `language` *(Optional, str)* – The preferred language for the response.

**Returns:** JSON response with the things.

##### `createThing(thingData: dict, language: str = None)`

Creates a new thing and adds it to the registry.

- `thingData` *(dict)* – The JSON object containing the thing data.
- `language` *(Optional, str)* – The preferred language for the response.

**Returns:** The API response.

##### `getThingByUID(thingUID: str, language: str = None)`

Gets a thing by UID.

- `thingUID` *(str)* – The UID of the thing.
- `language` *(Optional, str)* – The preferred language for the response.

**Returns:** JSON response with the thing data.

##### `updateThing(thingUID: str, thingData: dict, language: str = None)`

Updates a thing.

- `thingUID` *(str)* – The UID of the thing.
- `thingData` *(dict)* – The JSON object containing the updated thing data.
- `language` *(Optional, str)* – The preferred language for the response.

**Returns:** The API response.

##### `deleteThing(thingUID: str, force: bool = False, language: str = None)`

Removes a thing from the registry. Set 'force' to `true` if you want the thing to be removed immediately.

- `thingUID` *(str)* – The UID of the thing.
- `force` *(Optional, bool)* – If `True`, the thing will be immediately removed.
- `language` *(Optional, str)* – The preferred language for the response.

**Returns:** The API response.

##### `updateThingConfiguration(thingUID: str, configurationData: dict, language: str = None)`

Updates a thing's configuration.

- `thingUID` *(str)* – The UID of the thing.
- `configurationData` *(dict)* – The configuration data of the thing.
- `language` *(Optional, str)* – The preferred language for the response.

**Returns:** The API response.

##### `getThingConfigStatus(thingUID: str, language: str = None)`

Gets the thing's configuration status.

- `thingUID` *(str)* – The UID of the thing.
- `language` *(Optional, str)* – The preferred language for the response.

**Returns:** JSON response with the thing's configuration status.

##### `setThingStatus(thingUID: str, enabled: bool, language: str = None)`

Sets the thing's enabled status.

- `thingUID` *(str)* – The UID of the thing.
- `enabled` *(bool)* – If `True`, the thing will be enabled.
- `language` *(Optional, str)* – The preferred language for the response.

**Returns:** The API response.

##### `enableThing(thingUID: str)`

Enables the thing.

- `thingUID` *(str)* – The UID of the thing.

**Returns:** The API response.

##### `disableThing(thingUID: str)`

Disables the thing.

- `thingUID` *(str)* – The UID of the thing.

**Returns:** The API response.

##### `updateThingFirmware(thingUID: str, firmwareVersion: str, language: str = None)`

Updates the firmware of a thing.

- `thingUID` *(str)* – The UID of the thing.
- `firmwareVersion` *(str)* – The firmware version.
- `language` *(Optional, str)* – The preferred language for the response.

**Returns:** The API response.

##### `getThingFirmwareStatus(thingUID: str, language: str = None)`

Gets the thing's firmware status.

- `thingUID` *(str)* – The UID of the thing.
- `language` *(Optional, str)* – The preferred language for the response.

**Returns:** JSON response with the firmware status.

##### `getThingFirmwares(thingUID: str, language: str = None)`

Gets all available firmwares for the provided thing UID.

- `thingUID` *(str)* – The UID of the thing.
- `language` *(Optional, str)* – The preferred language for the response.

**Returns:** A list of available firmwares.

##### `getThingStatus(thingUID: str, language: str = None)`

Gets the thing's status.

- `thingUID` *(str)* – The UID of the thing.
- `language` *(Optional, str)* – The preferred language for the response.

**Returns:** JSON response with the thing's status.

### Transformations

The `Transformations` class provides methods to interact with transformations in the OpenHAB system via the REST API.

#### Methods

##### `getTransformations()`

Retrieves a list of all transformations.

**Returns:** A list of transformations (JSON).

##### `getTransformation(transformationUID: str)`

Gets a single transformation by its UID.

- `transformationUID` *(str)* – The UID of the transformation to retrieve.

**Returns:** The transformation (JSON).

##### `updateTransformation(transformationUID: str, transformationData)`

Updates a single transformation.

- `transformationUID` *(str)* – The UID of the transformation to update.
- `transformationData` *(dict)* – The new data for the transformation.

**Returns:** The response to the transformation update request (JSON).

##### `deleteTransformation(transformationUID: str)`

Deletes a single transformation by its UID.

- `transformationUID` *(str)* – The UID of the transformation to delete.

**Returns:** The response to the transformation delete request (JSON).

##### `getTransformationServices()`

Gets all transformation services available.

**Returns:** A list of transformation services (JSON).

### UI

The `UI` class provides methods to interact with UI components and tiles in the OpenHAB system via the REST API.

#### Methods

##### `getUiComponents(namespace: str, summary: bool = False)`

Retrieves all registered UI components within the specified namespace.

- `namespace` *(str)* – The namespace for which UI components should be retrieved.
- `summary` *(bool, optional)* – If True, only summary fields will be returned. Default is False.

**Returns:** A list of UI components (JSON).

##### `addUiComponent(namespace: str, componentData)`

Adds a UI component to the specified namespace.

- `namespace` *(str)* – The namespace where the UI component should be added.
- `componentData` *(dict)* – The data of the UI component to be added (JSON).

**Returns:** The response to the request (JSON).

##### `getUiComponent(namespace: str, componentUID: str)`

Retrieves a specific UI component in the specified namespace.

- `namespace` *(str)* – The namespace where the UI component is located.
- `componentUID` *(str)* – The UID of the UI component to retrieve.

**Returns:** The UI component (JSON).

##### `updateUiComponent(namespace: str, componentUID: str, componentData)`

Updates a specific UI component in the specified namespace.

- `namespace` *(str)* – The namespace where the UI component should be updated.
- `componentUID` *(str)* – The UID of the UI component to update.
- `componentData` *(dict)* – The new data for the UI component (JSON).

**Returns:** The response to the request (JSON).

##### `deleteUiComponent(namespace: str, componentUID: str)`

Removes a specific UI component from the specified namespace.

- `namespace` *(str)* – The namespace where the UI component should be removed.
- `componentUID` *(str)* – The UID of the UI component to delete.

**Returns:** The response to the request (JSON).

##### `getUiTiles()`

Retrieves all registered UI tiles.

**Returns:** A list of UI tiles (JSON).

### UUID

The `UUID` class provides a method to retrieve a unified unique identifier (UUID) from the OpenHAB system.

#### Methods

##### `getUUID()`

Retrieves a unified unique identifier (UUID) for the system.

**Returns:** A string containing the UUID.

### Voice

The `Voice` class provides methods to interact with the voice processing system, including starting and stopping dialogs, interpreting text, and speaking text aloud.

#### Methods

##### `getDefaultVoice()`

Gets the default voice used by the system.

**Returns:** A dictionary with details of the default voice.

##### `startDialog(sourceID: str, ksID: str = None, sttID: str = None, ttsID: str = None, voiceID: str = None, hliIDs: str = None, sinkID: str = None, keyword: str = None, listeningItem: str = None)`

Starts dialog processing for a given audio source.

**Parameters:**
- `sourceID` (str): The ID of the audio source.
- `ksID` (str, optional): The ID of the keyword spotter.
- `sttID` (str, optional): The ID of the speech-to-text system.
- `ttsID` (str, optional): The ID of the text-to-speech system.
- `voiceID` (str, optional): The ID of the voice.
- `hliIDs` (str, optional): A comma-separated list of interpreter IDs.
- `sinkID` (str, optional): The ID of the audio output.
- `keyword` (str, optional): The keyword used to start the dialog.
- `listeningItem` (str, optional): The name of the item to listen to.

**Returns:** The response from the server.

##### `stopDialog(sourceID: str)`

Stops dialog processing for a given audio source.

**Parameters:**
- `sourceID` (str): The ID of the audio source.

**Returns:** The response from the server.

##### `getInterpreters(language: str = None)`

Gets the list of all interpreters.

**Parameters:**
- `language` (str, optional): The language for the request.

**Returns:** A list of interpreters if successful.

##### `interpretText(text: str, language: str, IDs: list = None)`

Sends a text to the default human language interpreter.

**Parameters:**
- `text` (str): The text to be interpreted.
- `language` (str): The language of the text.
- `IDs` (list, optional): A list of interpreter IDs.

**Returns:** The response from the server.

##### `getInterpreter(interpreterID: str, language: str = None)`

Gets a single interpreter.

**Parameters:**
- `interpreterID` (str): The ID of the interpreter.
- `language` (str, optional): The language for the request.

**Returns:** The details of the interpreter.

##### `interpretTextBatch(text: str, language: str, IDs: list)`

Sends a text to a given human language interpreter(s).

**Parameters:**
- `text` (str): The text to be interpreted.
- `language` (str): The language of the text.
- `IDs` (list): A list of interpreter IDs.

**Returns:** The response from the server.

##### `listenAndAnswer(sourceID: str, sttID: str, ttsID: str, voiceID: str, hliIDs: list = None, sinkID: str = None, listeningItem: str = None)`

Executes a simple dialog sequence without keyword spotting for a given audio source.

**Parameters:**
- `sourceID` (str): The ID of the audio source.
- `sttID` (str): The ID of the speech-to-text system.
- `ttsID` (str): The ID of the text-to-speech system.
- `voiceID` (str): The ID of the voice.
- `hliIDs` (list, optional): A list of interpreter IDs.
- `sinkID` (str, optional): The ID of the audio output.
- `listeningItem` (str, optional): The name of the item to listen to.

**Returns:** The response from the server.

##### `sayText(text: str, voiceID: str, sinkID: str, volume: str = '100')`

Speaks a given text with a given voice through the given audio sink.

**Parameters:**
- `text` (str): The text to be spoken.
- `voiceID` (str): The ID of the voice.
- `sinkID` (str): The ID of the audio output.
- `volume` (str, optional): The volume level (default: `100`).

**Returns:** The response from the server.

##### `getVoices()`

Gets the list of all voices.

**Returns:** A list of voices if successful.

## Contributing

Contributions are welcome! Please create an issue or pull request to suggest changes.

We welcome contributions to improve **python-openhab-rest-client**!  

### How to contribute:  
1. Fork the repository.  
2. Create a new branch:  
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add your feature description"
   ```
4. Push to the branch:  
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.  

Please ensure your code adheres to PEP 8 guidelines and includes relevant documentation and tests. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  
