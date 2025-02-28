from .Client import OpenHABClient
import json
import requests


class Transformations:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Transformations class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getTransformations(self):
        """
        Get a list of all transformations.

        :return: A list of transformations (JSON).
        """
        try:
            response = self.client.get("/transformations")

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

    def getTransformation(self, transformationUID: str):
        """
        Get a single transformation.

        :param transformationUID: The transformationUID of the transformation to retrieve.

        :return: The transformation (JSON).
        """
        try:
            response = self.client.get(f"/transformations/{transformationUID}")

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

    def updateTransformation(self, transformationUID: str, transformationData):
        """
        Update a single transformation.

        :param transformationUID: The transformationUID of the transformation to update.
        :param transformationData: The new data for the transformation.

        :return: The response to the transformation update request (JSON).
        """
        try:
            response = self.client.put(f"/transformations/{transformationUID}", data=json.dumps(
                transformationData), header={"Content-Type": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Bad Request (content missing or invalid)"}
            elif status_code == 405:
                return {"error": "Transformation not editable."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Bad Request (content missing or invalid)"}
        elif status_code == 405:
            return {"error": "Transformation not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def deleteTransformation(self, transformationUID: str):
        """
        Delete a single transformation.

        :param transformationUID: The transformationUID of the transformation to delete.

        :return: The response to the transformation update request (JSON) or status/error message.
        """
        try:
            response = self.client.delete(
                f"/transformations/{transformationUID}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Transformation not editable."}
            elif status_code == 404:
                return {"error": "UID not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "UID not found."}
        elif status_code == 405:
            return {"error": "Transformation not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def getTransformationServices(self):
        """
        Get all transformation services.

        :return: A list of transformation services (JSON).
        """
        try:
            response = self.client.get("/transformations/services")

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
