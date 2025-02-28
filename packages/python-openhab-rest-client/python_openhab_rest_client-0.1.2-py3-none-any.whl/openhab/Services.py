from .Client import OpenHABClient
import json
import requests


class Services:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Services class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getServices(self, language=None):
        """
        Get all configurable services.

        :param language: Optional language setting (as header).

        :return: A list of services (JSON).
        """
        try:
            response = self.client.get(
                "/services", header={"Accept-Language": language} if language else {})

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

    def getService(self, serviceID: str, language=None):
        """
        Get configurable service for the given service ID.

        :param serviceID: The ID of the service to retrieve.
        :param language: Optional language setting (as header).

        :return: The service object (JSON).
        """
        try:
            response = self.client.get(
                f"/services/{serviceID}", header={"Accept-Language": language} if language else {})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def getServiceConfig(self, serviceID: str):
        """
        Get service configuration for the given service ID.

        :param serviceID: The ID of the service.

        :return: The configuration of the service (JSON).
        """
        try:
            response = self.client.get(f"/services/{serviceID}/config")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 500:
                return {"error": "Configuration can not be read due to internal error."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 500:
            return {"error": "Configuration can not be read due to internal error."}

        return {"error": f"Unexpected response: {status_code}"}

    def updateServiceConfig(self, serviceID: str, configData: dict):
        """
        Updates a service configuration for the given service ID and returns the old configuration.

        :param serviceID: The ID of the service.
        :param configData: The new configuration data (as a dictionary).

        :return: The old configuration of the service (JSON).
        """
        try:
            response = self.client.put(f"/services/{serviceID}/config", data=json.dumps(
                configData), header={"Content-Type": "application/json", "Accept": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 500:
                return {"error": "Configuration can not be updated due to internal error."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 204:
            return {"error": "No old configuration."}
        elif status_code == 500:
            return {"error": "Configuration can not be updated due to internal error."}

        return {"error": f"Unexpected response: {status_code}"}

    def deleteServiceConfig(self, serviceID: str):
        """
        Deletes a service configuration for the given service ID and returns the old configuration.

        :param serviceID: The ID of the service.

        :return: The old configuration of the service (JSON).
        """
        try:
            response = self.client.delete(
                f"/services/{serviceID}/config", header={"Accept": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 500:
                return {"error": "Configuration can not be updated due to internal error."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 204:
            return {"error": "No old configuration."}
        elif status_code == 500:
            return {"error": "Configuration can not be updated due to internal error."}

        return {"error": f"Unexpected response: {status_code}"}

    def getServiceContexts(self, serviceID: str, language=None):
        """
        Get existing multiple context service configurations for the given factory PID.

        :param serviceID: The ID of the service.
        :param language: Optional language setting (as header).

        :return: A list of contexts (JSON).
        """
        header = {"Accept": "application/json"}  # Default to application/json
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f"/services/{serviceID}/contexts", header=header)

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
