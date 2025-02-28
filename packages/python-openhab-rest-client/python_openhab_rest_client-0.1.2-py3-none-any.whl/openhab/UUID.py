from .Client import OpenHABClient
import requests


class UUID:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the UUID class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getUUID(self) -> str:
        """
        A unified unique id.

        :return: The UUID as String.
        """
        try:
            response = self.client.get("/uuid")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response.strip()

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}
