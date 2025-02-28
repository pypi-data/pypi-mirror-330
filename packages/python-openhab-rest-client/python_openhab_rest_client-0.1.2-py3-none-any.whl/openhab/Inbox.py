from .Client import OpenHABClient
import requests


class Inbox:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Inbox class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllDiscoveredThings(self, includeIgnored: bool = True) -> list:
        """
        Get all discovered things.

        :param includeIgnored: Whether ignored entries should also be included (default: True).

        :return: A list of discovered things with details such as UID, flag, label, and properties.
        """
        try:
            response = self.client.get(
                "/inbox", params={"includeIgnored": str(includeIgnored).lower()})

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

    def removeDiscoveryResult(self, thingUID: str) -> dict:
        """
        Removes the discovery result from the inbox.

        :param thingUID: The UID of the discovered thing to be removed.

        :return: The API response to the delete request.
        """
        try:
            response = self.client.delete(f"/inbox/{thingUID}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Discovery result not found in the inbox."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Discovery result not found in the inbox."}

        return {"error": f"Unexpected response: {status_code}"}

    def approveDiscoveryResult(self, thingUID: str, thingLabel: str, newThingID: str = None, language: str = None) -> dict:
        """
        Approves the discovery result by adding the thing to the registry.

        :param thingUID: The UID of the discovered thing.
        :param thingLabel: The new name of the thing.
        :param newThingID: Optional: The new thing ID.
        :param language: Optional: Language preference for the response.

        :return: The API response to the approval request.
        """
        try:
            response = self.client.post(f"/inbox/{thingUID}/approve", header={"Accept-Language": language, "Content-Type": "text/plain"} if language else {
                                        "Content-Type": "text/plain"}, params={"newThingID": newThingID} if newThingID else {}, data=thingLabel)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Invalid new thing ID."}
            elif status_code == 404:
                return {"error": "Thing unable to be approved."}
            elif status_code == 409:
                return {"error": "No binding found that supports this thing."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Invalid new thing ID."}
        elif status_code == 404:
            return {"error": "Thing unable to be approved."}
        elif status_code == 409:
            return {"error": "No binding found that supports this thing."}

        return {"error": f"Unexpected response: {status_code}"}

    def ignoreDiscoveryResult(self, thingUID: str) -> dict:
        """
        Flags a discovery result as ignored for further processing.

        :param thingUID: The UID of the discovered thing.

        :return: The API response to the ignore request.
        """
        try:
            response = self.client.post(f"/inbox/{thingUID}/ignore")

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

    def unignoreDiscoveryResult(self, thingUID: str) -> dict:
        """
        Removes the ignore flag from a discovery result.

        :param thingUID: The UID of the discovered thing.

        :return: The API response to the unignore request.
        """
        try:
            response = self.client.post(f"/inbox/{thingUID}/unignore")

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
