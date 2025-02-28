import requests
import json


class OpenHABClient:
    def __init__(self, url: str, username: str = None, password: str = None, token: str = None):
        """
        Initializes the OpenHABClient instance.

        :param url: The base URL of the OpenHAB server (e.g., "http://127.0.0.1:8080").
        :param username: Optional; The username for Basic Authentication (default is None).
        :param password: Optional; The password for Basic Authentication (default is None).
        :param token: Optional; The Bearer Token for Token-based Authentication (default is None).
        """
        self.url = url.rstrip("/")  # Remove trailing slash if present
        self.username = username
        self.password = password
        self.token = token
        self.isCloud = False
        self.isLoggedIn = False

        self.session = requests.Session()

        if self.token:
            # Use Token-based authentication
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            })
        elif self.username and self.password:
            # Use Basic Authentication
            self.auth = (self.username, self.password)
            self.session.auth = self.auth
        else:
            self.auth = None

        self.__login()

    def __login(self):
        """
        Attempts to log in to the openHAB server.

        If the server is "myopenhab.org", it sets the connection to the cloud service.
        Otherwise, it prepares a local connection and verifies login credentials.
        """
        if self.url == "https://myopenhab.org":
            self.isCloud = True
        else:
            self.isCloud = False

        # Check connection and authentication
        try:
            loginResponse = self.session.get(self.url + "/rest", timeout=8)
            loginResponse.raise_for_status()

            if loginResponse.ok or loginResponse.status_code == 200:
                self.isLoggedIn = True
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP error occurred: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Connection error occurred: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout occurred: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request exception occurred: {err}")

    def __executeRequest(self, header: dict = None, resourcePath: str = None, method: str = None, data=None, params=None):
        """
        Executes an HTTP request to the openHAB server.

        :param header: Optional; A dictionary of headers to be sent with the request.
        :param resourcePath: The path of the resource to interact with.
        :param method: The HTTP method (GET, POST, PUT, DELETE).
        :param data: Optional; The data to send in the request (for POST and PUT requests).
        :return: The response of the request, either as JSON or plain text.

        :raises ValueError: If the method is invalid or if the resource path is not provided.
        """
        if not resourcePath or not method:
            raise ValueError(
                'You must specify a valid resource path and HTTP method!')

        method = method.lower()
        header = header or {}

        if resourcePath[0] != "/":
            resourcePath = "/" + resourcePath

        # Ensure resource path starts with "/rest"
        if not resourcePath.startswith("/rest"):
            resourcePath = f"/rest{resourcePath}"
        
        url = f"{self.url}{resourcePath}"

        # Update session headers
        self.session.headers.update(header)
        """
        try:
            url = f"{self.url}{resourcePath}"
            if method == "get":
                response = self.session.get(url, params=params, timeout=5)
            elif method == "post":
                response = self.session.post(
                    url, data=data, params=params, timeout=5)
            elif method == "put":
                response = self.session.put(
                    url, data=data, params=params, timeout=5)
            elif method == "delete":
                response = self.session.delete(
                    url, data=data, params=params, timeout=5)
            else:
                raise ValueError("Invalid HTTP method provided!")

            response.raise_for_status()

            # Prüfen, ob die Antwort JSON enthält
            if response.text.strip():  # Wenn die Antwort nicht leer ist
                if "application/json" in response.headers.get("Content-Type", ""):
                    return response.json()  # JSON dekodieren
                else:
                    return response.text  # Anderen Text zurückgeben

            # Nur Status zurückgeben, wenn keine Antwort vorhanden ist
            return {"status": response.status_code}
        except requests.exceptions.RequestException as err:
            print(f"Request error occurred: {err}")
            raise
        """
        if method == "get":
            response = self.session.get(url, params=params, headers=header, timeout=5)
        elif method == "post":
            response = self.session.post(url, data=data, params=params, headers=header, timeout=5)
        elif method == "put":
            response = self.session.put(url, data=data, params=params, headers=header, timeout=5)
        elif method == "delete":
            response = self.session.delete(url, data=data, params=params, headers=header, timeout=5)
        else:
            raise ValueError("Invalid HTTP method provided!")

        # Pass on mistakes directly instead of catching them here!
        response.raise_for_status()

        # If the response is empty, but there was still no error, we return the status code
        if not response.text.strip():
            return {"status": response.status_code}

        # Return JSON response, if available
        if "application/json" in response.headers.get("Content-Type", ""):
            return response.json()
        
        return response.text  # Fallback: Return text response

    def __executeSSE(self, url: str):
        """
        Executes a Server-Sent Events (SSE) request.

        :param url: The URL to connect to for the SSE stream.

        :return: The response object with the SSE stream.
        """
        if self.username is not None and self.password is not None:
            return self.session.get(url, auth=self.auth, stream=True)
        else:
            return self.session.get(url, stream=True)

    def __executeSSE(self, url: str, header: dict = {}):
        """
        Executes a Server-Sent Events (SSE) request with custom headers.

        :param url: The URL to connect to for the SSE stream.
        :param header: A dictionary of headers to include in the request.

        :return: The response object with the SSE stream.
        """
        if self.username is not None and self.password is not None:
            return self.session.get(url, auth=self.auth, headers=header, stream=True)
        else:
            return self.session.get(url, headers=header, stream=True)

    def get(self, endpoint: str, header: dict = None, params: dict = None):
        """
        Sends a GET request to the openHAB server.

        :param endpoint: The endpoint for the GET request (e.g., "/items").
        :param header: Optional; Headers to be sent with the request.
        :param params: Optional; Query parameters for the GET request.

        :return: The response from the GET request, either as JSON or plain text.
        """
        return self.__executeRequest(header, endpoint, "get", params=params)

    def post(self, endpoint: str, header: dict = None, data=None, params: dict = None):
        """
        Sends a POST request to the openHAB server.

        :param endpoint: The endpoint for the POST request (e.g., "/items").
        :param header: Optional; Headers to be sent with the request.
        :param data: Optional; The data to send in the POST request.
        :param params: Optional; Query parameters for the request.

        :return: The response from the POST request.
        """
        return self.__executeRequest(header, endpoint, "post", data=data, params=params)

    def put(self, endpoint: str, header: dict = None, data=None, params: dict = None):
        """
        Sends a PUT request to the openHAB server.

        :param endpoint: The endpoint for the PUT request (e.g., "/items").
        :param header: Optional; Headers to be sent with the request.
        :param data: Optional; The data to send in the PUT request.
        :param params: Optional; Query parameters for the request.

        :return: The response from the PUT request.
        """
        return self.__executeRequest(header, endpoint, "put", data=data)

    def delete(self, endpoint: str, header: dict = None, data=None, params: dict = None):
        """
        Sends a DELETE request to the openHAB server.

        :param endpoint: The endpoint for the DELETE request (e.g., "/items").
        :param header: Optional; Headers to be sent with the request.
        :param data: Optional; The data to send in the DELETE request.
        :param params: Optional; Query parameters for the request.

        :return: The response from the DELETE request.
        """
        return self.__executeRequest(header, endpoint, "delete", data=data, params=params)
