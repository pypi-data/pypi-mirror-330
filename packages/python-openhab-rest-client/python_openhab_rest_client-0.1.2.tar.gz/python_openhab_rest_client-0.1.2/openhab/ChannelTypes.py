from .Client import OpenHABClient
import requests


class ChannelTypes:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ChannelTypes class with an OpenHABClient instance.

        :param client: An instance of OpenHABClient used for REST API communication.
        """
        self.client = client

    def getAllChannelTypes(self, language: str = None, prefixes: str = None) -> list:
        """
        Retrieves all available channel types.

        :param language: Optional header 'Accept-Language' to specify the preferred language.
        :param prefixes: Optional query parameter to filter channel types by prefix.

        :return: A list of channel types.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        params = {}
        if prefixes:
            params["prefixes"] = prefixes

        try:
            response = self.client.get(
                "/channel-types", header=header, params=params)

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

    def getChannelTypeByUID(self, channelTypeUID: str, language: str = None) -> dict:
        """
        Retrieves the item types the given trigger channel type UID can be linked to.

        :param channelTypeUID: The unique UID of the channel type.
        :param language: Optional header 'Accept-Language' to specify the preferred language.

        :return: Details of the specific channel type.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f"/channel-types/{channelTypeUID}", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Channel type with provided channelTypeUID does not exist."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Channel type with provided channelTypeUID does not exist."}

        return {"error": f"Unexpected response: {status_code}"}

    def getLinkableItemTypes(self, channelTypeUID: str) -> list:
        """
        Retrieves the item types that can be linked to the specified trigger channel type.

        :param channelTypeUID: The unique UID of the channel type.

        :return: A list of item types.
        """

        try:
            response = self.client.get(
                f"/channel-types/{channelTypeUID}/linkableItemTypes")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 204:
                return {"error": "No content: channel type has no linkable items or is no trigger channel."}
            elif status_code == 404:
                return {"error": "Given channel type UID not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Given channel type UID not found."}
        elif status_code == 204:
            return {"error": "No content: channel type has no linkable items or is no trigger channel."}

        return {"error": f"Unexpected response: {status_code}"}
