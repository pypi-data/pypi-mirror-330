from .Client import OpenHABClient
import json
import requests


class Tags:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Tags class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getTags(self, language=None):
        """
        Get all available semantic tags.

        :param language: Optional header for language setting.

        :return: A list of semantic tags (JSON).
        """
        try:
            response = self.client.get(
                "/tags", header={"Accept-Language": language} if language else {})

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

    def createTag(self, tagData, language=None):
        """
        Creates a new semantic tag and adds it to the registry.

        :param tagData: The data object for the tag to be created.
        :param language: Optional header for language setting.

        :return: The response to the tag creation request (JSON).
        """
        header = {"Content-Type": "application/json",
                  "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.post(
                "/tags", data=json.dumps(tagData), header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "The tag identifier is invalid or the tag label is missing."}
            elif status_code == 409:
                return {"error": "A tag with the same identifier already exists."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 201:
            return {"message": "Created"}
        elif status_code == 400:
            return {"error": "The tag identifier is invalid or the tag label is missing."}
        elif status_code == 409:
            return {"error": "A tag with the same identifier already exists."}

        return {"error": f"Unexpected response: {status_code}"}

    def getTag(self, tagID: str, language=None):
        """
        Gets a semantic tag and its sub-tags.

        :param tagID: The ID of the tag to retrieve.
        :param language: Optional header for language setting.

        :return: The tag object and its sub-tags (JSON).
        """
        header = {"Content-Type": "application/json",
                  "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(f"/tags/{tagID}", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Semantic tag not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Semantic tag not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def updateTag(self, tagID: str, tagData, language=None):
        """
        Updates a semantic tag.

        :param tagID: The ID of the tag to be updated.
        :param tagData: The new tag data.
        :param language: Optional header for language setting.

        :return: The response to the tag update request (JSON).
        """
        header = {"Content-Type": "application/json",
                  "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.put(
                f"/tags/{tagID}", data=json.dumps(tagData), header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Semantic tag not editable."}
            elif status_code == 404:
                return {"error": "Semantic tag not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Semantic tag not found."}
        elif status_code == 405:
            return {"error": "Semantic tag not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def deleteTag(self, tagID: str, language=None):
        """
        Removes a semantic tag and its sub-tags from the registry.

        :param tagID: The ID of the tag to be removed.
        :param language: Optional header for language setting.

        :return: The response to the tag deletion request (JSON).
        """
        header = {"Content-Type": "application/json",
                  "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.delete(f"/tags/{tagID}", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Semantic tag not removable."}
            elif status_code == 404:
                return {"error": "Semantic tag not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK, was deleted."}
        elif status_code == 404:
            return {"error": "Semantic tag not found."}
        elif status_code == 405:
            return {"error": "Semantic tag not removable."}

        return {"error": f"Unexpected response: {status_code}"}
