from .Client import OpenHABClient
import requests


class ThingTypes:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ThingTypes class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllThingTypes(self, bindingID: str = None, language: str = None) -> list:
        """
        Gets all available thing types without config description, channels, and properties.

        :param bindingID: (Optional) Filter by binding ID.
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A list of thing types.
        """
        header = {"Content-Type": "application/json"}
        params = {}
        if bindingID:
            params["bindingId"] = bindingID
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                "/thing-types", header=header, params=params)

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

    def getThingType(self, thingTypeUID: str, language: str = None) -> dict:
        """
        Gets a thing type by UID.

        :param thingTypeUID: The UID of the thing type.
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A dictionary with the details of the thing type or an empty response with status 204.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f"/thing-types/{thingTypeUID}", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "No Content."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "No Content."}

        return {"error": f"Unexpected response: {status_code}"}
