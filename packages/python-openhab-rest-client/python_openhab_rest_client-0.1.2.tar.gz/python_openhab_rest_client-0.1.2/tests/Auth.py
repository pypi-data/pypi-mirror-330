import json
import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient
from openhab.tests import AuthTest

if __name__ == "__main__":
    # Initialize OpenHAB client (replace with your OpenHAB URL and authentication details)
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    authTest = AuthTest(client)

    tokenName = "openhab"

    grantType="authorization_code"  # Specify the grant type
    code="test-auth-code"           # Replace with a valid authorization code
    redirectURI="http://localhost"  # Replace with the actual redirect URI
    clientID="test-client-id"       # Replace with a valid client ID

    # Run all tests
    authTest.testGetAPITokens()               # Test #1
    authTest.testRevokeAPIToken(tokenName)  # Test #2
    authTest.testGetSessions()                # Test #3
    tokenResponse = authTest.testGetToken(
        grantType=grantType,
        code=code,
        redirectURI=redirectURI,
        clientID=clientID
    )                                       # Test #4
    authTest.testLogout(tokenResponse)      # Test #5
