from .Client import OpenHABClient
import json
import requests


class UI:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the UI class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getUIComponents(self, namespace: str, summary: bool = False):
        """
        Get all registered UI components in the specified namespace.

        :param namespace: The namespace for which UI components should be retrieved.
        :param summary: If True, only summary fields will be returned.

        :return: A list of UI components (JSON).
        """
        try:
            response = self.client.get(
                f"/ui/components/{namespace}", params={'summary': summary} if summary else {})

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

    def addUIComponent(self, namespace: str, componentData):
        """
        Add a UI component in the specified namespace.

        :param namespace: The namespace where the UI component should be added.
        :param componentData: The data of the UI component (JSON) to be added.

        :return: The response to the request (JSON).
        """
        try:
            response = self.client.post(f"/ui/components/{namespace}", data=json.dumps(
                componentData), header={"Content-Type": "application/json"})

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

    def getUIComponent(self, namespace: str, componentUID: str):
        """
        Get a specific UI component in the specified namespace.

        :param namespace: The namespace where the UI component is located.
        :param componentUID: The UID of the UI component to retrieve.

        :return: The UI component (JSON).
        """
        try:
            response = self.client.get(
                f"/ui/components/{namespace}/{componentUID}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Component not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Component not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def updateUIComponent(self, namespace: str, componentUID: str, componentData):
        """
        Update a specific UI component in the specified namespace.

        :param namespace: The namespace where the UI component should be updated.
        :param componentUID: The UID of the UI component to update.
        :param componentData: The new data for the UI component (JSON).

        :return: The response to the request (JSON).
        """
        try:
            response = self.client.put(
                f"/ui/components/{namespace}/{componentUID}", data=json.dumps(componentData), header={"Content-Type": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Component not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Component not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def deleteUIComponent(self, namespace: str, componentUID: str):
        """
        Remove a specific UI component in the specified namespace.

        :param namespace: The namespace where the UI component should be removed.
        :param componentUID: The UID of the UI component to delete.

        :return: The response to the request (JSON).
        """
        try:
            response = self.client.delete(
                f"/ui/components/{namespace}/{componentUID}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Component not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Component not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def getUITiles(self):
        """
        Get all registered UI tiles.

        :return: A list of UI tiles (JSON).
        """
        try:
            response = self.client.get("/ui/tiles")

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
