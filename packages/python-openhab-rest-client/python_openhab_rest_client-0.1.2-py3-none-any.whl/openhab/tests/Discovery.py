import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Discovery

class DiscoveryTest:
    def __init__(self, client: OpenHABClient):
        self.discoveryAPI = Discovery(client)

    # Test fetching all discovery bindings
    def testGetAllDiscoveryBindings(self):
        print("\n~~~~ Test #1: getAllDiscoveryBindings() ~~~~\n")

        try:
            response = self.discoveryAPI.getAllDiscoveryBindings()
            print("Bindings supporting discovery:", response)
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test starting a discovery scan for a specific binding
    def testStartBindingScan(self, bindingID: str):
        print("\n~~~~ Test #2: startBindingScan() ~~~~\n")

        try:
            timeout = self.discoveryAPI.startBindingScan(bindingID=bindingID)
            print(f"Discovery started. Timeout: {timeout} seconds")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
