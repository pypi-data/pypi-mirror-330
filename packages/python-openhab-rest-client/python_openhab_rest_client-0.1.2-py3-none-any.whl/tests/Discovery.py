import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient
from openhab.tests import DiscoveryTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    discoveryTest = DiscoveryTest(client)

    # Define test variables
    bindingID = "network"

    # Run all tests
    discoveryTest.testGetAllDiscoveryBindings()        # Test #1
    discoveryTest.testStartBindingScan(bindingID)      # Test #2
