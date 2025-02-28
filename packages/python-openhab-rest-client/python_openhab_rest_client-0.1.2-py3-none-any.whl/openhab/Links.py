from .Client import OpenHABClient
import json
from urllib.parse import quote
import requests


class Links:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Links class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllLinks(self, channelUID: str = None, itemName: str = None) -> list:
        """
        Gets all available links.

        :param channelUID: Optional; Filters by the Channel UID.
        :param itemName: Optional; Filters by the Item Name.

        :return: A list of links containing details such as ItemName, ChannelUID, and configuration.
        """
        params = {}
        if channelUID:
            params["channelUID"] = channelUID
        if itemName:
            params["itemName"] = itemName

        try:
            response = self.client.get(
                "/links", params=params, header={"Content-Type": "application/json"})

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

    def getIndividualLink(self, itemName: str, channelUID: str) -> dict:
        """
        Retrieves an individual link.

        :param itemName: The name of the item.
        :param channelUID: The UID of the channel.

        :return: The link with details of the item, channel UID, and configuration.
        """
        itemName = quote(itemName, safe="")
        channelUID = quote(channelUID, safe="")

        try:
            response = self.client.get(
                f"/links/{itemName}/{channelUID}", header={"Accept": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Content does not match the path."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Content does not match the path."}

        return {"error": f"Unexpected response: {status_code}"}

    def linkItemToChannel(self, itemName: str, channelUID: str, configuration: dict) -> dict:
        """
        Links an item to a channel.

        :param itemName: The name of the item.
        :param channelUID: The UID of the channel.
        :param configuration: The configuration for the link.

        :return: The API response when the link is successfully created.
        """
        itemName = quote(itemName, safe="")
        channelUID = quote(channelUID, safe="")

        try:
            response = self.client.put(f"/links/{itemName}/{channelUID}", data=json.dumps(
                {"itemName": itemName, "channelUID": channelUID, "configuration": configuration}), header={"Content-Type": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Link is not editable."}
            elif status_code == 400:
                return {"error": "Content does not match the path."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Content does not match the path."}
        elif status_code == 405:
            return {"error": "Link is not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def unlinkItemFromChannel(self, itemName: str, channelUID: str) -> dict:
        """
        Unlinks an item from a channel.

        :param itemName: The name of the item.
        :param channelUID: The UID of the channel.

        :return: The API response when the link is successfully removed.
        """
        itemName = quote(itemName, safe="")
        channelUID = quote(channelUID, safe="")

        try:
            response = self.client.delete(
                f"/links/{itemName}/{channelUID}", header={"Content-Type": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Link not editable."}
            elif status_code == 404:
                return {"error": "Link not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Link not found."}
        elif status_code == 405:
            return {"error": "Link not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def deleteAllLinks(self, object: str) -> dict:
        """
        Delete all links that refer to an item or thing.

        :param object: The name of the item or the UID of the thing.

        :return: The API response when all links are successfully deleted.
        """
        try:
            response = self.client.delete(f"/links/{object}")

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

    def getOrphanLinks(self) -> list:
        """
        Get orphan links between items and broken/non-existent thing channels.

        :return: A list of orphan links.
        """
        try:
            response = self.client.get(
                "/links/orphans", header={"Accept": "application/json"})

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

    def purgeUnusedLinks(self) -> dict:
        """
        Remove unused/orphaned links.

        :return: The API response when the links are successfully removed.
        """
        try:
            response = self.client.post("/links/purge")

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
