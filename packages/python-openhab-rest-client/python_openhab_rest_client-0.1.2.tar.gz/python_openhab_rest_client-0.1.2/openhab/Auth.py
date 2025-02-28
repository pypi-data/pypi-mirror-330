from urllib.parse import urlencode
from .Client import OpenHABClient
import json
import requests


class Auth:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Auth class with an OpenHABClient instance.

        :param client: An instance of OpenHABClient used for REST API communication.
        """
        self.client = client

    def getAPITokens(self, language: str = None) -> dict:
        """
        Retrieve the API tokens associated with the authenticated user.

        :param language: (Optional) Language setting for the API request.

        :return: JSON response from the server.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get("/auth/apitokens", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 401:
                return {"error": "User is not authenticated."}
            elif status_code == 404:
                return {"error": "User not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "User not found."}
        elif status_code == 401:
            return {"error": "User is not authenticated."}

        return {"error": f"Unexpected response: {status_code}"}

    def revokeAPIToken(self, tokenName: str, language: str = None) -> dict:
        """
        Revoke a specific API token associated with the authenticated user.

        :param tokenName: Name of the API token to be revoked.
        :param language: (Optional) Language setting for the API request.

        :return: JSON response from the server.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.delete(
                f"/auth/apitokens/{tokenName}", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 401:
                return {"error": "User is not authenticated."}
            elif status_code == 404:
                return {"error": "User not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "User not found."}
        elif status_code == 401:
            return {"error": "User is not authenticated."}

        return {"error": f"Unexpected response: {status_code}"}

    def logout(self, refreshToken: str, language: str = None) -> dict:
        """
        Terminate the session associated with a refresh token.

        :param refreshToken: The refresh token used to delete the session.
        :param language: (Optional) Language setting for the API request.

        :return: JSON response from the server.
        """
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.post(
                "/auth/logout", header=header, data=json.dumps({"refresh_token": refreshToken}))

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 401:
                return {"error": "User is not authenticated."}
            elif status_code == 404:
                return {"error": "User not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "User not found."}
        elif status_code == 401:
            return {"error": "User is not authenticated."}

        return {"error": f"Unexpected response: {status_code}"}

    def getSessions(self, language: str = None) -> dict:
        """
        Retrieve the sessions associated with the authenticated user.

        :param language: (Optional) Language setting for the API request.

        :return: JSON response from the server.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get("/auth/sessions", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 401:
                return {"error": "User is not authenticated."}
            elif status_code == 404:
                return {"error": "User not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "User not found."}
        elif status_code == 401:
            return {"error": "User is not authenticated."}

        return {"error": f"Unexpected response: {status_code}"}

    def getToken(self, grantType: str, code: str = None, redirectURI: str = None, clientID: str = None, refreshToken: str = None, codeVerifier: str = None, language: str = None) -> dict:
        """
        Obtain access and refresh tokens.

        :param grantType: The type of grant being requested.
        :param code: (Optional) Authorization code for authentication.
        :param redirectUri: (Optional) Redirect URI for OAuth authentication.
        :param clientID: (Optional) Client ID for authentication.
        :param refreshToken: (Optional) Refresh token for token renewal.
        :param codeVerifier: (Optional) Code verifier for PKCE authentication.
        :param language: (Optional) Language setting for the API request.

        :return: JSON response from the server.
        """
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }

        body = {
            "grant_type": grantType,
            "code": code,
            "redirect_uri": redirectURI,
            "client_id": clientID,
            "refresh_token": refreshToken,
            "code_verifier": codeVerifier
        }
        # Remove all None values
        body = {k: v for k, v in body.items() if v is not None}

        # Encode as application/x-www-form-urlencoded
        encodedBody = urlencode(body)

        try:
            response = self.client.post(
                "/auth/token", header=header, data=encodedBody)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Invalid request parameters."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Invalid request parameters."}

        return {"error": f"Unexpected response: {status_code}"}
