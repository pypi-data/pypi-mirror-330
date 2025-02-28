from .Client import OpenHABClient
import json
import requests


class Events:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Events class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllEvents(self, topics: str = None) -> list:
        """
        Get all available events, optionally filtered by topic.

        :param topics: A comma-separated list of topics to filter the events by.

        :return: A SSE stream of events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events" + (f"?topics={topics}" if topics else ""))

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Topic is empty or contains invalid characters."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Topic is empty or contains invalid characters."}

        return {"error": f"Unexpected response: {status_code}"}

    def initiateStateTracker(self) -> str:
        """
        Initiates a new item state tracker connection.

        :return: The connection ID as a string.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + "/rest/events/states", header={"Accept": "*/*"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def updateSSEConnectionItems(self, connectionID: str, items: list) -> str:
        """
        Changes the list of items a SSE connection will receive state updates for.

        :param connectionID: The ID of the existing connection.
        :param items: A SSE stream of item names to subscribe to for state updates.

        :return: A success message when the update is completed.
        """
        try:
            response = self.client.post(f"/rest/events/states/{connectionID}", data=json.dumps(
                items), header={"Content-Type": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Unknown connectionID."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Unknown connectionID."}

        return {"error": f"Unexpected response: {status_code}"}


class ItemEvents:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ItemEvents class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def ItemEvent(self):
        """
        Get all item-related events.

        :return: A SSE stream of item events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/items")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def ItemAddedEvent(self, itemName: str = "*"):
        """
        Get events for added items.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of added item events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/items/{itemName}/added")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def ItemRemovedEvent(self, itemName: str = "*"):
        """
        Get events for removed items.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of removed item events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/items/{itemName}/removed")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def ItemUpdatedEvent(self, itemName: str = "*"):
        """
        Get events for updated items.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of updated item events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/items/{itemName}/updated")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def ItemCommandEvent(self, itemName: str = "*"):
        """
        Get events for item commands.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of item command events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/items/{itemName}/command")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def ItemStateEvent(self, itemName: str = "*"):
        """
        Get events for item state changes.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of item state events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/items/{itemName}/state")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def ItemStatePredictedEvent(self, itemName: str = "*"):
        """
        Get events for predicted item state changes.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of item state predicted events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/items/{itemName}/statepredicted")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def ItemStateChangedEvent(self, itemName: str = "*"):
        """
        Get events for item state changes.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of item state changed events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/items/{itemName}/statechanged")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def GroupItemStateChangedEvent(self, itemName: str, memberName: str):
        """
        Get events for state changes of group items.

        :param itemName: The name of the item.
        :param memberName: The name of the group member.

        :return: A SSE stream of group item state changed events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/items/{itemName}/{memberName}/statechanged")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}


class ThingEvents:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ThingEvents class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def ThingAddedEvent(self, thingUID: str = "*"):
        """
        Get events for added things.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of added thing events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/added")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def ThingRemovedEvent(self, thingUID: str = "*"):
        """
        Get events for removed things.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of removed thing events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/removed")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def ThingUpdatedEvent(self, thingUID: str = "*"):
        """
        Get events for updated things.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of updated thing events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/updated")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def ThingStatusInfoEvent(self, thingUID: str = "*"):
        """
        Get events for thing status information.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of thing status information events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/status")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def ThingStatusInfoChangedEvent(self, thingUID: str = "*"):
        """
        Get events for thing status information changes.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of thing status information changed events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/statuschanged")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}


class InboxEvents:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the InboxEvents class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def InboxAddedEvent(self, thingUID: str = "*"):
        """
        Get events for added things in the inbox.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of added inbox events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/inbox/{thingUID}/added")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def InboxRemovedEvent(self, thingUID: str = "*"):
        """
        Get events for removed things in the inbox.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of removed inbox events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/inbox/{thingUID}/removed")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def InboxUpdatedEvent(self, thingUID: str = "*"):
        """
        Get events for updated things in the inbox.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of updated inbox events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/inbox/{thingUID}/updated")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}


class LinkEvents:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the LinkEvents class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def ItemChannelLinkAddedEvent(self, itemName: str = "*", channelUID: str = "*"):
        """
        Get events for added item-channel links.

        :param itemName: The name of the item (default is "*").
        :param channelUID: The UID of the channel (default is "*").

        :return: A SSE stream of added item-channel link events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/links/{itemName}-{channelUID}/added")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def ItemChannelLinkRemovedEvent(self, itemName: str = "*", channelUID: str = "*"):
        """
        Get events for removed item-channel links.

        :param itemName: The name of the item (default is "*").
        :param channelUID: The UID of the channel (default is "*").

        :return: A SSE stream of removed item-channel link events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/links/{itemName}-{channelUID}/removed")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}


class ChannelEvents:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ChannelEvents class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def ChannelDescriptionChangedEvent(self, channelUID: str = "*"):
        """
        Get events for changes in channel descriptions.

        :param channelUID: The UID of the channel (default is "*").

        :return: A SSE stream of channel description changed events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/channels/{channelUID}/descriptionchanged")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def ChannelTriggeredEvent(self, channelUID: str = "*"):
        """
        Get events for triggered channels.

        :param channelUID: The UID of the channel (default is "*").

        :return: A SSE stream of channel triggered events.
        """
        try:
            response = self.client._OpenHABClient__executeSSE(
                self.client.url + f"/rest/events?topics=openhab/channels/{channelUID}/triggered")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}
