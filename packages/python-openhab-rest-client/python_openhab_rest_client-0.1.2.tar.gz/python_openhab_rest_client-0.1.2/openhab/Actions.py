from .Client import OpenHABClient
import json
import requests


class Actions:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Actions class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllActions(self, thingUID: str, language: str = None) -> list:
        """
        Get all available actions for provided thing UID.

        :param thingUID: The UID of the thing for which actions are to be retrieved.
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A list of actions.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(f"/actions/{thingUID}", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 204:
                return {"error": "No actions found."}
            elif status_code == 404:
                return {"error": f"Thing not found: {thingUID}"}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 204:
            return {"error": "No actions found."}
        elif status_code == 404:
            return {"error": f"Thing not found: {thingUID}"}

        return {"error": f"Unexpected response: {status_code}"}

    def executeAction(self, thingUID: str, actionUID: str, actionInputs: dict, language: str = None) -> str:
        """
        Executes a thing action.

        :param thingUID: The UID of the thing on which the action is to be executed.
        :param actionUID: The UID of the action to be executed.
        :param actionInputs: The inputs for the action as a dictionary.
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A response from the server.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.post(
                f"/actions/{thingUID}/{actionUID}", header=header, data=json.dumps(actionInputs))

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Action not found."}
            elif status_code == 500:
                return {"error": "Creation of action handler or execution failed."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Action not found."}
        elif status_code == 500:
            return {"error": "Creation of action handler or execution failed."}

        return {"error": f"Unexpected response: {status_code}"}
