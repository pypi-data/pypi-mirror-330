import json
from .Client import OpenHABClient
import urllib.parse
import requests


class Addons:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Addons class with an OpenHABClient instance.

        :param client: An instance of OpenHABClient used for REST API communication.
        """
        self.client = client

    def getAddons(self, serviceID: str = None, language: str = None) -> dict:
        """
        Retrieves a list of all available add-ons.

        :param serviceID: Optional service ID to filter the results.
        :param language: Optional language preference for the response.

        :return: A dictionary containing the add-ons data.
        """
        params = {"serviceId": serviceID} if serviceID else {}
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get("/addons", header=header, params=params)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Service not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Service not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def getAddon(self, addonID: str, serviceID: str = None, language: str = None) -> dict:
        """
        Retrieves details of a specific add-on by its ID.

        :param addonID: The unique identifier of the add-on.
        :param serviceID: Optional service ID to filter the results.
        :param language: Optional language preference for the response.

        :return: A dictionary containing details of the specified add-on.
        """
        params = {"serviceId": serviceID} if serviceID else {}
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f"/addons/{addonID}", header=header, params=params)

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

    def getAddonConfig(self, addonID: str, serviceID: str = None) -> dict:
        """
        Retrieves the configuration of a specific add-on.

        :param addonID: The unique identifier of the add-on.
        :param serviceID: Optional service ID to filter the results.

        :return: A dictionary containing the configuration of the specified add-on.
        """
        params = {"serviceId": serviceID} if serviceID else {}

        try:
            response = self.client.get(
                f"/addons/{addonID}/config", header={"Content-Type": "application/json"}, params=params)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 500:
                return {"error": "Configuration can not be read due to internal error."}
            elif status_code == 404:
                return {"error": "Add-on does not exist."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Add-on does not exist."}
        elif status_code == 500:
            return {"error": "Configuration can not be read due to internal error."}

        return {"error": f"Unexpected response: {status_code}"}

    def updateAddonConfig(self, addonID: str, configData: dict, serviceID: str = None) -> dict:
        """
        Updates the configuration of a specific add-on and returns the updated configuration.

        :param addonID: The unique identifier of the add-on.
        :param configData: A dictionary containing the new configuration settings.
        :param serviceID: Optional service ID to specify the target service.

        :return: A dictionary containing the updated configuration.
        """
        data = {
            **configData}  # Create a copy to avoid modifying the original dictionary
        if serviceID:
            data["serviceId"] = serviceID

        try:
            response = self.client.put(
                f"/addons/{addonID}/config", header={"Content-Type": "application/json"}, data=json.dumps(data))

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 500:
                return {"error": "Configuration can not be updated due to internal error."}
            elif status_code == 404:
                return {"error": "Add-on does not exist."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Add-on does not exist."}
        elif status_code == 500:
            return {"error": "Configuration can not be updated due to internal error."}

        return {"error": f"Unexpected response: {status_code}"}

    def installAddon(self, addonID: str, serviceID: str = None, language: str = None) -> dict:
        """
        Installs an add-on by its ID.

        :param addonID: The unique identifier of the add-on.
        :param serviceID: Optional service ID to specify the target service.
        :param language: Optional language preference for the response.

        :return: A dictionary containing the installation status.
        """
        data = {"serviceId": serviceID} if serviceID else {}
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.post(
                f"/addons/{addonID}/install", header=header, data=data)

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

    def uninstallAddon(self, addonID: str, serviceID: str = None, language: str = None) -> dict:
        """
        Uninstalls an add-on by its ID.

        :param addonID: The unique identifier of the add-on.
        :param serviceID: Optional service ID to specify the target service.
        :param language: Optional language preference for the response.

        :return: A dictionary containing the uninstallation status.
        """
        data = {"serviceId": serviceID} if serviceID else {}
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.post(
                f"/addons/{addonID}/uninstall", header=header, data=data)

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

    def getAddonServices(self, language: str = None) -> dict:
        """
        Retrieves a list of all available add-on services.

        :param language: Optional language preference for the response.

        :return: A dictionary containing the available add-on services.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                "/addons/services", header=header, params=None)

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

    def getAddonSuggestions(self, language: str = None) -> dict:
        """
        Retrieves a list of suggested add-ons for installation.

        :param language: Optional language preference for the response.

        :return: A dictionary containing suggested add-ons.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                "/addons/suggestions", header=header, params=None)

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

    def getAddonTypes(self, language: str = None) -> dict:
        """
        Retrieves a list of all available add-on types.

        :param language: Optional language preference for the response.

        :return: A dictionary containing available add-on types.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                "/addons/types", header=header, params=None)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Service not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Service not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def installAddonFromUrl(self, url: str) -> dict:
        """
        Installs an add-on from a given URL.

        :param url: The URL of the add-on to install.

        :return: A dictionary containing the installation status.
        """
        encoded_url = urllib.parse.quote(url, safe='')  # Encode the URL
        endpoint = f"/addons/url/{encoded_url}/install"

        try:
            response = self.client.post(
                endpoint, header={"Content-Type": "text/plain"}, data=None)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "The given URL is malformed or not valid."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "The given URL is malformed or not valid."}

        return {"error": f"Unexpected response: {status_code}"}
