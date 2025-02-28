from .Client import OpenHABClient
import requests


class ConfigDescriptions:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ConfigDescriptions class with an OpenHABClient instance.

        :param client: An instance of OpenHABClient used for REST API communication.
        """
        self.client = client

    def getAllConfigDescriptions(self, language: str = None, scheme: str = None) -> list:
        """
        Retrieves all available config descriptions.

        :param language: Optional header 'Accept-Language' to specify the preferred language.
        :param scheme: Optional query parameter to filter results by a specific scheme.

        :return: A list of configuration descriptions.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        params = {}
        if scheme:
            params["scheme"] = scheme

        try:
            response = self.client.get(
                "/config-descriptions", header=header, params=params)

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

    def getConfigDescriptionByURI(self, uri: str, language: str = None) -> dict:
        """
        Retrieves a config description by URI.

        :param uri: The URI of the requested configuration description.
        :param language: Optional header 'Accept-Language' to specify the preferred language.

        :return: Details of the specific configuration description.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f"/config-descriptions/{uri}", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Invalid URI syntax."}
            elif status_code == 404:
                return {"error": "Not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Not found."}
        elif status_code == 400:
            return {"error": "Invalid URI syntax."}

        return {"error": f"Unexpected response: {status_code}"}
