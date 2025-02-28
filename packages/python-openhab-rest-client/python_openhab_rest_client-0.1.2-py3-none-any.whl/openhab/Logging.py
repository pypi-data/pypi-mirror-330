from .Client import OpenHABClient
import json
import requests


class Logging:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Logging class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllLoggers(self) -> dict:
        """
        Get all loggers.

        :return: A list of loggers with names and levels.
        """
        try:
            response = self.client.get("/logging")

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

    def getSingleLogger(self, loggerName: str) -> dict:
        """
        Get a single logger.

        :param loggerName: The name of the logger.

        :return: The logger with the specified name and level.
        """
        try:
            response = self.client.get(f"/logging/{loggerName}")

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

    def modifyOrAddLogger(self, loggerName: str, level: str) -> dict:
        """
        Modify or add a logger.

        :param loggerName: The name of the logger.
        :param level: The level of the logger.

        :return: The API response after modification or addition.
        """
        data = {
            "loggerName": loggerName,
            "level": level
        }

        try:
            response = self.client.put(
                f"/logging/{loggerName}", data=json.dumps(data), header={"Content-Type": "application/json"})

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

    def removeLogger(self, loggerName: str) -> dict:
        """
        Remove a single logger.

        :param loggerName: The name of the logger.

        :return: The API response after removing the logger.
        """
        try:
            response = self.client.delete(f"/logging/{loggerName}")

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
