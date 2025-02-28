from .Client import OpenHABClient
import requests


class Iconsets:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Iconsets class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllIconsets(self, language: str = None) -> list:
        """
        Gets all icon sets.

        :param language: Optional language preference for the response (e.g. 'en', 'de').

        :return: A list of icon sets with details such as ID, label, description and supported formats.
        """
        try:
            response = self.client.get(
                "/iconsets", header={"Accept-Language": language} if language else {})

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
