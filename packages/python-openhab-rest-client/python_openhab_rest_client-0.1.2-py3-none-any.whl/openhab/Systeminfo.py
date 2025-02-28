from .Client import OpenHABClient
import requests


class Systeminfo:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Systeminfo class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getSystemInfo(self, language: str = None):
        """
        Gets information about the system.

        :return: A Dictionary with system informations.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get("/systeminfo", header=header)

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

    def getUoMInfo(self, language: str = None):
        """
        Get all supported dimensions and their system units.

        :return: A Dictionary with UOM informations.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get("/systeminfo/uom", header=header)

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
