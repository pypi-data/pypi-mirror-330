from .Client import OpenHABClient
import json
import requests


class Items:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Items class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllItems(
        self,
        language: str = None,
        type: str = None,
        tags: str = None,
        metadata: str = ".*",
        recursive: bool = False,
        fields: str = None,
        staticDataOnly: bool = False,
    ):
        """
        Get all available items.

        :param language: Optional; Language filter for header "Accept-Language".
        :param type: Optional; Item type filter.
        :param tags: Optional; Item tag filter.
        :param metadata: Optional; Metadata selector (default: .*).
        :param recursive: Optional; Whether to fetch group members recursively (default: False).
        :param fields: Optional; Limit to specific fields (comma-separated).
        :param staticDataOnly: Optional; Only returns cached data (default: False).

        :return: A dictionary or list containing the item data as returned by the API.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        params = {
            "type": type,
            "tags": tags,
            "metadata": metadata,
            "recursive": str(recursive).lower(),
            "fields": fields,
            "staticDataOnly": str(staticDataOnly).lower(),
        }

        # Remove None values from parameters
        params = {key: value for key,
                  value in params.items() if value is not None}

        try:
            response = self.client.get("/items", header=header, params=params)

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

    def addOrUpdateItems(self, items: list):
        """
        Adds a list of items to the registry or updates the existing items.

        :param items: A list of item data (Dictionary).

        :return: A response object or confirmation that the items were successfully added or updated.
        """
        try:
            response = self.client.put(
                "/items", data=json.dumps(items), header={"Content-Type": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Payload is invalid."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Payload is invalid."}

        return {"error": f"Unexpected response: {status_code}"}

    def getItem(self, itemName: str, language: str = None, metadata: str = ".*", recursive: bool = True):
        """
        Gets a single item.

        :param itemName: The name of the item.
        :param language: Optional; Language filter for header "Accept-Language".
        :param metadata: Optional; Metadata selector (default: .*).
        :param recursive: Optional; Whether to fetch group members recursively (default: True).

        :return: A dictionary containing the requested item data.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        params = {
            "metadata": metadata,
            "recursive": str(recursive).lower(),
        }

        try:
            response = self.client.get(
                f"/items/{itemName}", header=header, params=params)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Item not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def addOrUpdateItem(self, itemName: str, itemData: dict, language: str = None):
        """
        Adds a new item to the registry or updates the existing item.

        :param itemName: The name of the item.
        :param itemData: The data of the item (Dictionary).
        :param language: Optional; Language filter for header "Accept-Language".

        :return: A response object or confirmation that the item was successfully added or updated.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.put(
                f"/items/{itemName}", header=header, data=json.dumps(itemData))

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Payload invalid."}
            elif status_code == 404:
                return {"error": "Item not found or name in path invalid."}
            elif status_code == 405:
                return {"error": "Item not editable."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 201:
            return {"message": "Item created."}
        elif status_code == 400:
            return {"error": "Payload invalid."}
        elif status_code == 404:
            return {"error": "Item not found or name in path invalid."}
        elif status_code == 405:
            return {"error": "Item not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def sendCommand(self, itemName: str, command: str):
        """
        Sends a command to an item.

        :param itemName: The name of the item.
        :param command: The command to be sent (e.g., ON, OFF).

        :return: A response object or confirmation that the command was successfully sent.
        """
        try:
            response = self.client.post(f"/items/{itemName}", header={
                                        "Content-Type": "text/plain; charset=utf-8", "Accept": "text/plain"}, data=command)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Item command null."}
            elif status_code == 404:
                return {"error": "Item not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}
        elif status_code == 400:
            return {"error": "Item command null."}

        return {"error": f"Unexpected response: {status_code}"}

    def postUpdate(self, itemName: str, state: str):
        """
        Updates the state of an item.

        :param itemName: The name of the item.
        :param state: The state to be signaled for the item.

        :return: A response object or confirmation that the state was successfully updated.
        """
        return self.updateItemState(itemName, state)

    def deleteItem(self, itemName: str):
        """
        Removes an item from the registry.

        :param itemName: The name of the item.

        :return: A response object or confirmation that the item was successfully deleted.
        """
        try:
            response = self.client.delete(f"/items/{itemName}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Item not found or item is not editable."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found or item is not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def addGroupMember(self, itemName: str, memberItemName: str):
        """
        Adds a new member to a group item.

        :param itemName: The name of the group item.
        :param memberItemName: The name of the member item.

        :return: A response object or confirmation that the group member was successfully added.
        """
        try:
            response = self.client.put(
                f"/items/{itemName}/members/{memberItemName}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Member item is not editable."}
            elif status_code == 404:
                return {"error": "Item or member item not found or item is not of type group item."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item or member item not found or item is not of type group item."}
        elif status_code == 405:
            return {"error": "Member item is not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def removeGroupMember(self, itemName: str, memberItemName: str):
        """
        Removes an existing member from a group item.

        :param itemName: The name of the group item.
        :param memberItemName: The name of the member item.

        :return: A response object or confirmation that the group member was successfully removed.
        """
        try:
            response = self.client.delete(
                f"/items/{itemName}/members/{memberItemName}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Member item is not editable."}
            elif status_code == 404:
                return {"error": "Item or member item not found or item is not of type group item."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item or member item not found or item is not of type group item."}
        elif status_code == 405:
            return {"error": "Member item is not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def addMetadata(self, itemName: str, namespace: str, metadata: dict):
        """
        Adds metadata to an item.

        :param itemName: The name of the item.
        :param namespace: The namespace of the metadata.
        :param metadata: A dictionary containing the metadata.

        :return: A response object or confirmation that the metadata was successfully added.
        """
        try:
            response = self.client.put(f"/items/{itemName}/metadata/{namespace}", header={
                                       "Content-Type": "application/json"}, data=json.dumps(metadata))

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Metadata value empty."}
            elif status_code == 405:
                return {"error": "Metadata not editable."}
            elif status_code == 404:
                return {"error": "Item not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 201:
            return {"message": "Created."}
        elif status_code == 400:
            return {"error": "Metadata value empty."}
        elif status_code == 404:
            return {"error": "Item not found."}
        elif status_code == 405:
            return {"error": "Metadata not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def removeMetadata(self, itemName: str, namespace: str):
        """
        Removes metadata from an item.

        :param itemName: The name of the item.
        :param namespace: The namespace of the metadata.

        :return: A response object or confirmation that the metadata was successfully removed.
        """
        try:
            response = self.client.delete(
                f"/items/{itemName}/metadata/{namespace}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Meta data not editable."}
            elif status_code == 404:
                return {"error": "Item not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}
        elif status_code == 405:
            return {"error": "Meta data not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def getMetadataNamespaces(self, itemName: str, language: str = None):
        """
        Gets the namespaces of an item.

        :param itemName: The name of the item.
        :param language: Optional; Language filter for header "Accept-Language".

        :return: A list of namespaces associated with the item.
        """
        header = {"Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f"/items/{itemName}/metadata/namespaces", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Item not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def getSemanticItem(self, itemName: str, semanticClass: str, language: str = None):
        """
        Gets the item that defines the requested semantics of an item.

        :param itemName: The name of the item.
        :param semanticClass: The requested semantic class.
        :param language: Optional; Language filter for header "Accept-Language".

        :return: A dictionary containing the semantic item data.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f"/items/{itemName}/semantic/{semanticClass}", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Item not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def getItemState(self, itemName: str):
        """
        Gets the state of an item.

        :param itemName: The name of the item.

        :return: A dictionary containing the current state of the item.
        """
        try:
            response = self.client.get(f"/items/{itemName}/state")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Item not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def updateItemState(self, itemName: str, state: str, language: str = None):
        """
        Updates the state of an item.

        :param itemName: The name of the item.
        :param state: The new state of the item.
        :param language: Optional; Language filter for header "Accept-Language".

        :return: A response object or confirmation that the state was successfully updated.
        """
        header = {"Content-Type": "text/plain; charset=utf-8",
                  "Accept": "text/plain"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.put(
                f"/items/{itemName}/state", header=header, data=state)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Item state null."}
            elif status_code == 404:
                return {"error": "Item not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 202:
            return {"message": "Accepted."}
        elif status_code == 404:
            return {"error": "Item not found."}
        elif status_code == 400:
            return {"error": "Item state null."}

        return {"error": f"Unexpected response: {status_code}"}

    def addTag(self, itemName: str, tag: str):
        """
        Adds a tag to an item.

        :param itemName: The name of the item.
        :param tag: The tag to be added.

        :return: A response object or confirmation that the tag was successfully added.
        """
        try:
            response = self.client.put(f"/items/{itemName}/tags/{tag}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Item not editable."}
            elif status_code == 404:
                return {"error": "Item not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}
        elif status_code == 405:
            return {"error": "Item not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def removeTag(self, itemName: str, tag: str):
        """
        Removes a tag from an item.

        :param itemName: The name of the item.
        :param tag: The tag to be removed.

        :return: A response object or confirmation that the tag was successfully removed.
        """
        try:
            response = self.client.delete(f"/items/{itemName}/tags/{tag}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Item not editable."}
            elif status_code == 404:
                return {"error": "Item not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}
        elif status_code == 405:
            return {"error": "Item not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def purgeOrphanedMetadata(self):
        """
        Remove unused/orphaned metadata.

        :return: A response object or confirmation that orphaned metadata was successfully purged.
        """
        try:
            response = self.client.post("/items/metadata/purge")

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
