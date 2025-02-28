from .Client import OpenHABClient
import json
import requests


class Persistence:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Persistence class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllServices(self) -> dict:
        """
        Gets a list of persistence services.

        :return: A list of persistence services with IDs, labels, and types.
        """
        try:
            response = self.client.get("/persistence")

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

    def getServiceConfiguration(self, serviceID: str) -> dict:
        """
        Gets a persistence service configuration.

        :param serviceID: The ID of the persistence service.

        :return: The configuration of the service.
        """
        try:
            response = self.client.get(f"/persistence/{serviceID}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Service configuration not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Service configuration not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def setServiceConfiguration(self, serviceID: str, config: dict) -> dict:
        """
        Sets a persistence service configuration.

        :param serviceID: The ID of the persistence service.
        :param config: The configuration data.

        :return: The response from the API after modification.
        """
        try:
            config["serviceId"] = serviceID  

            response = self.client.put(
                f"/persistence/{serviceID}",
                data=json.dumps(config),
                headers={"Content-Type": "application/json", "Accept": "application/json"}
            )

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Payload invalid."}
            elif status_code == 405:
                return {"error": "PersistenceServiceConfiguration not editable."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 201:
            return {"message": "PersistenceServiceConfiguration created."}
        elif status_code == 400:
            return {"error": "Payload invalid."}
        elif status_code == 405:
            return {"error": "PersistenceServiceConfiguration not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def deleteServiceConfiguration(self, serviceID: str) -> dict:
        """
        Deletes a persistence service configuration.

        :param serviceID: The ID of the persistence service.

        :return: The response from the API after deleting the configuration.
        """
        try:
            response = self.client.delete(f"/persistence/{serviceID}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Payload invalid."}
            elif status_code == 405:
                return {"error": "PersistenceServiceConfiguration not editable."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Payload invalid."}
        elif status_code == 405:
            return {"error": "PersistenceServiceConfiguration not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def getItemsForService(self, serviceID: str) -> dict:
        """
        Gets a list of items available via a specific persistence service.

        :param serviceID: The ID of the persistence service.

        :return: A list of items with their last and earliest timestamps.
        """
        try:
            response = self.client.get(
                f"/persistence/items?serviceID={serviceID}")

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

    def getItemPersistenceData(self, serviceID: str, itemName: str, startTime: str = None, endTime: str = None, page: int = 1, pageLength: int = 50) -> dict:
        """
        Gets item persistence data from the persistence service.

        :param serviceID: The ID of the persistence service.
        :param itemName: The name of the item.
        :param startTime: The start time for the data. Defaults to 1 day before `endTime`.
        :param endTime: The end time for the data. Defaults to the current time.
        :param page: The page of data. Defaults to `1`.
        :param pageLength: The number of data points per page. Defaults to `50`.

        :return: The retrieved data points of the item.
        """
        try:
            response = self.client.get(f"/persistence/items/{itemName}", params={
                                       "serviceID": serviceID, "starttime": startTime, "endtime": endTime, "page": page, "pagelength": pageLength})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Unknown Item or persistence service."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Unknown Item or persistence service."}

        return {"error": f"Unexpected response: {status_code}"}

    def storeItemData(self, serviceID: str, itemName: str, time: str, state: str) -> dict:
        """
        Stores item persistence data into the persistence service.

        :param serviceID: The ID of the persistence service.
        :param itemName: The name of the item.
        :param time: The time of the storage.
        :param state: The state of the item to be stored.

        :return: The response from the API after storing the data.
        """
        try:
            response = self.client.put(f"/persistence/items/{itemName}", params={
                                       "serviceID": serviceID, "time": time, "state": state})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Unknown Item or persistence service."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Unknown Item or persistence service."}

        return {"error": f"Unexpected response: {status_code}"}

    def deleteItemData(self, serviceID: str, itemName: str, startTime: str, endTime: str) -> dict:
        """
        Deletes item persistence data from a specific persistence service in a given time range.

        :param serviceID: The ID of the persistence service.
        :param itemName: The name of the item.
        :param startTime: The start time of the data to be deleted.
        :param endTime: The end time of the data to be deleted.

        :return: The response from the API after deleting the data.
        """
        try:
            response = self.client.delete(f"/persistence/items/{itemName}", params={
                                          "serviceID": serviceID, "starttime": startTime, "endtime": endTime})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Invalid filter parameters."}
            elif status_code == 404:
                return {"error": "Unknown persistence service."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Unknown persistence service."}
        elif status_code == 400:
            return {"error": "Invalid filter parameters."}

        return {"error": f"Unexpected response: {status_code}"}
