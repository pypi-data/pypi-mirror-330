import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, UUID

class UUIDTest:
    def __init__(self, client: OpenHABClient):
        self.uuidAPI = UUID(client)

    # Retrieve the UUID
    def testGetUuid(self):
        """Test retrieving the OpenHAB UUID"""
        print("\n~~~~ Test #1: getUUID() ~~~~\n")

        try:
            openhabUUID = self.uuidAPI.getUUID()
            print(f"The OpenHAB UUID is: {openhabUUID}")
        except Exception as e:
            print(f"Error fetching UUID: {e}")
