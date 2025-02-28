from .Client import OpenHABClient
import json
import requests


class Things:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Things class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllThings(self, summary: bool = False, staticDataOnly: bool = False, language: str = None):
        """
        Get all available things.

        :param summary: If True, returns only the summary fields.
        :param staticDataOnly: If True, returns a cacheable list.
        :param language: The preferred language for the response.

        :return: JSON response with the things.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                '/things', params={'summary': summary, 'staticDataOnly': staticDataOnly}, header=header)

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

    def createThing(self, thingData: dict, language: str = None):
        """
        Creates a new thing and adds it to the registry.

        :param thingData: The JSON object containing the thing data.
        :param language: The preferred language for the response.

        :return: The API response.
        """
        header = {"Content-Type": "application/json",
                  "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.post(
                '/things', data=json.dumps(thingData), header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 409:
                return {"error": "A thing with the same uid already exists."}
            elif status_code == 400:
                return {"error": "A uid must be provided, if no binding can create a thing of this type."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "A uid must be provided, if no binding can create a thing of this type."}
        elif status_code == 409:
            return {"error": "A thing with the same uid already exists."}

        return {"error": f"Unexpected response: {status_code}"}

    def getThingByUID(self, thingUID: str, language: str = None):
        """
        Gets a thing by UID.

        :param thingUID: The UID of the thing.
        :param language: The preferred language for the response.

        :return: JSON response with the thing data.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(f'/things/{thingUID}', header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Thing not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "THing not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def updateThing(self, thingUID: str, thingData: dict, language: str = None):
        """
        Updates a thing.

        :param thingUID: The UID of the thing.
        :param thingData: The JSON object containing the updated thing data.
        :param language: The preferred language for the response.

        :return: The API response.
        """
        header = {"Content-Type": "application/json",
                  "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.put(
                f'/things/{thingUID}', data=json.dumps(thingData), header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 409:
                return {"error": "Thing could not be updated as it is not editable."}
            elif status_code == 404:
                return {"error": "Thing not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Thing not found."}
        elif status_code == 409:
            return {"error": "Thing could not be updated as it is not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def deleteThing(self, thingUID: str, force: bool = False, language: str = None):
        """
        Removes a thing from the registry. Set 'force' to __true__ if you want the thing to be removed immediately.

        :param thingUID: The UID of the thing.
        :param force: If True, the thing will be immediately removed.
        :param language: The preferred language for the response.

        :return: The API response.
        """
        try:
            response = self.client.delete(f'/things/{thingUID}', params={'force': force}, header={
                                          'Accept-Language': language} if language else {})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 409:
                return {"error": "Thing could not be deleted because it's not editable."}
            elif status_code == 404:
                return {"error": "Thing not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK, was deleted."}
        elif status_code == 202:
            return {"message": "ACCEPTED for asynchronous deletion."}
        elif status_code == 404:
            return {"error": "Thing not found."}
        elif status_code == 409:
            return {"error": "Thing could not be deleted because it's not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def updateThingConfiguration(self, thingUID: str, configurationData: dict, language: str = None):
        """
        Updates a thing's configuration.

        :param thingUID: The UID of the thing.
        :param configurationData: The configuration data of the thing.
        :param language: The preferred language for the response.

        :return: The API response.
        """
        header = {"Content-Type": "application/json",
                  "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.put(
                f'/things/{thingUID}/config', data=json.dumps(configurationData), header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Configuration of the thing is not valid."}
            elif status_code == 404:
                return {"error": "Thing not found."}
            elif status_code == 409:
                return {"error": "Thing could not be updated as it is not editable."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Configuration of the thing is not valid."}
        elif status_code == 404:
            return {"error": "Thing not found."}
        elif status_code == 409:
                return {"error": "Thing could not be updated as it is not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def getThingConfigStatus(self, thingUID: str, language: str = None):
        """
        Gets the thing's configuration status.

        :param thingUID: The UID of the thing.
        :param language: The preferred language for the response.

        :return: JSON response with the thing's configuration status.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f'/things/{thingUID}/config/status', header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Thing not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Thing not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def setThingStatus(self, thingUID: str, enabled: bool, language: str = None):
        """
        Sets the thing's enabled status.

        :param thingUID: The UID of the thing.
        :param enabled: If True, the thing will be enabled.
        :param language: The preferred language for the response.

        :return: The API response.
        """
        header = {"Content-Type": "text/plain"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.put(
                f'/things/{thingUID}/enable', data="true" if enabled else "false", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Thing not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Thing not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def enableThing(self, thingUID: str):
        return self.setThingStatus(thingUID, True)

    def disableThing(self, thingUID: str):
        return self.setThingStatus(thingUID, False)

    def updateThingFirmware(self, thingUID: str, firmwareVersion: str, language: str = None):
        """
        Updates the firmware of a thing.

        :param thingUID: The UID of the thing.
        :param firmwareVersion: The firmware version.
        :param language: The preferred language for the response.

        :return: The API response.
        """
        header = {"Content-Type": "application/json",
                  "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.put(
                f'/things/{thingUID}/firmware/{firmwareVersion}', header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Firmware update preconditions not satisfied."}
            elif status_code == 404:
                return {"error": "Thing not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Thing not found."}
        elif status_code == 400:
            return {"error": "Firmware update preconditions not satisfied."}

        return {"error": f"Unexpected response: {status_code}"}

    def getThingFirmwareStatus(self, thingUID: str, language: str = None):
        """
        Gets the thing's firmware status.

        :param thingUID: The UID of the thing.
        :param language: The preferred language for the response.

        :return: JSON response with the firmware status.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f'/things/{thingUID}/firmware/status', header=header)

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
        elif status_code == 204:
            return {"error": "No firmware status provided by this Thing."}

        return {"error": f"Unexpected response: {status_code}"}

    def getThingFirmwares(self, thingUID: str, language: str = None):
        """
        Gets all available firmwares for the provided thing UID.

        :param thingUID: The UID of the thing.
        :param language: The preferred language for the response.

        :return: A list of available firmwares.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f'/things/{thingUID}/firmwares', header=header)

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
        elif status_code == 204:
            return {"error": "No firmwares found."}

        return {"error": f"Unexpected response: {status_code}"}

    def getThingStatus(self, thingUID: str, language: str = None):
        """
        Gets the thing's status.

        :param thingUID: The UID of the thing.
        :param language: The preferred language for the response.

        :return: JSON response with the thing's status.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f'/things/{thingUID}/status', header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Thing not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Thing not found."}

        return {"error": f"Unexpected response: {status_code}"}
