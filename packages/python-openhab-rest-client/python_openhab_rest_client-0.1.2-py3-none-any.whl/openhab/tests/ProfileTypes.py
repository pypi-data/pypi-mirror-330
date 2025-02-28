import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, ProfileTypes

class ProfileTypesTest:
    def __init__(self, client: OpenHABClient):
        self.profileTypesAPI = ProfileTypes(client)

    def testGetProfileTypes(self):
        """ Retrieve all available profile types """
        print("\n~~~~ Test #1 getProfileTypes() ~~~~\n")
        try:
            profile_types = self.profileTypesAPI.getProfileTypes()
            print(json.dumps(profile_types, indent=4))
        except Exception as e:
            print(f"Error retrieving profile types: {e}")
