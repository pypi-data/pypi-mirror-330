import json
import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Auth

class AuthTest:
    def __init__(self, client: OpenHABClient):
        self.authAPI = Auth(client)

    def testGetAPITokens(self, language: str = None):
        """Test retrieving all API tokens."""
        print("\n~~~~ Test #1: getApiTokens() ~~~~\n")
        
        try:
            tokens = self.authAPI.getAPITokens(language)
            print("API Tokens:", json.dumps(tokens, indent=4))
        except Exception as e:
            print(f"Error retrieving API tokens: {e}")

    def testRevokeAPIToken(self, tokenName: str, language: str = None):
        """Test revoking an API token."""
        print("\n~~~~ Test #2: revokeApiToken() ~~~~\n")

        try:
            revokeResponse = self.authAPI.revokeAPIToken(tokenName, language)
            print("Token revoked:", json.dumps(revokeResponse, indent=4))
        except Exception as e:
            print(f"Error revoking API token: {e}")

    def testGetSessions(self, language: str = None):
        """Test retrieving active sessions."""
        print("\n~~~~ Test #3: getSessions() ~~~~\n")

        try:
            sessions = self.authAPI.getSessions(language)
            print("Sessions:", json.dumps(sessions, indent=4))
        except Exception as e:
            print(f"Error retrieving sessions: {e}")

    def testGetToken(self, grantType: str, code: str = None, redirectURI: str = None, clientID: str = None, refreshToken: str = None, codeVerifier: str = None, language: str = None):
        """Test obtaining an access token using the authorization code flow."""
        print("\n~~~~ Test #4: getToken(grantType, code, redirectUri, clientID, refreshToken, codeVerifier) ~~~~\n")

        try:
            tokenResponse = self.authAPI.getToken(grantType=grantType, code=code, redirectURI=redirectURI, clientID=clientID, refreshToken=refreshToken, codeVerifier=codeVerifier, language=language)

            if "error" in tokenResponse:
                print(f"Error in token response: {tokenResponse['error']}")
            else:
                print("Token Response:", json.dumps(tokenResponse, indent=4))
            return tokenResponse  # Return response for further testing
        except Exception as e:
            print(f"Exception occurred while retrieving token: {e}")
            return None

    def testLogout(self, tokenResponse: dict, language: str = None):
        """Test logging out using a valid refresh token."""
        print("\n~~~~ Test #5: logout() ~~~~\n")

        if tokenResponse and "refresh_token" in tokenResponse:
            refreshToken = tokenResponse["refresh_token"]
            try:
                logoutResponse = self.authAPI.logout(refreshToken=refreshToken, language=language)
                print("Logout Response:", json.dumps(logoutResponse, indent=4))
            except Exception as e:
                print(f"Error during logout: {e}")
        else:
            print("No refresh token available. Logout not possible.")
