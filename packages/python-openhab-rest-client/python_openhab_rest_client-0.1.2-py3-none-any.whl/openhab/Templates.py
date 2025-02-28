from .Client import OpenHABClient
import requests


class Templates:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Templates class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllTemplates(self, language: str = None) -> list:
        """
        Get all available templates.

        :param language: (Optional) Language setting for the Accept-Language header.
        :return: A list of templates.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get("/templates", header=header)

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

    def getTemplateByUID(self, templateUID: str, language: str = None) -> dict:
        """
        Gets a template corresponding to the given UID.

        :param templateUID: The UID of the template.
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A dictionary with the details of the template.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f"/templates/{templateUID}", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Template corresponding to the given UID does not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Template corresponding to the given UID does not found."}

        return {"error": f"Unexpected response: {status_code}"}
