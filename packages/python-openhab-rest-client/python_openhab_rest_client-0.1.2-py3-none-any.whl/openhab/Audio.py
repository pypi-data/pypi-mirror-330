from .Client import OpenHABClient
import requests


class Audio:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Audio class with an OpenHABClient object.

        :param client: An instance of OpenHABClient used for REST API communication.
        """
        self.client = client

    def getDefaultSink(self, language: str = None):
        """
        Retrieves the default sink if defined, or the first available sink.

        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A dictionary containing information about the default sink.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get("/audio/defaultsink", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Sink not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Sink not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def getDefaultSource(self, language: str = None):
        """
        Retrieves the default source if defined, or the first available source.

        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A dictionary containing information about the default source.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get("/audio/defaultsource", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Sink not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Service not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def getSinks(self, language: str = None):
        """
        Retrieves a list of all available sinks.

        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A list of available sinks.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get("/audio/sinks", header=header)

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

    def getSources(self, language: str = None):
        """
        Retrieves a list of all available sources.

        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A list of available sources.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get("/audio/sources", header=header)

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
