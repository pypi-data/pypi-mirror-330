from .Client import OpenHABClient
import requests


class ProfileTypes:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ProfileTypes class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getProfileTypes(self, channelTypeUID=None, itemType=None, language: str = None):
        """
        Gets all available profile types.

        :param channelTypeUID: Optional filter for the channel type.
        :param itemType: Optional filter for the item type.
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A list of profile types.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        params = {}
        if channelTypeUID:
            params["channelTypeUID"] = channelTypeUID
        if itemType:
            params["itemType"] = itemType

        try:
            response = self.client.get(
                "/profile-types", params=params, header=header)

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
