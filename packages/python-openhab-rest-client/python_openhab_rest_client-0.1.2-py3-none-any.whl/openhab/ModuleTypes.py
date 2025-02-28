from .Client import OpenHABClient
import requests


class ModuleTypes:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ModuleTypes class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getModuleTypes(self, tags=None, typeFilter=None, language: str = None):
        """
        Get all available module types.

        :param tags: Optional filter for tags.
        :param typeFilter: Optional filter for the type (action, condition, trigger).
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A list of module types.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        params = {}
        if tags:
            params["tags"] = tags
        if typeFilter:
            params["type"] = typeFilter

        try:
            response = self.client.get(
                "/module-types", params=params, header=header)

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

    def getModuleType(self, moduleTypeUID, language: str = None):
        """
        Gets a module type corresponding to the given UID.

        :param moduleTypeUID: The UID of the module type.
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A dictionary with the module type information.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f"/module-types/{moduleTypeUID}", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Module Type corresponding to the given UID does not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Module Type corresponding to the given UID does not found."}

        return {"error": f"Unexpected response: {status_code}"}
