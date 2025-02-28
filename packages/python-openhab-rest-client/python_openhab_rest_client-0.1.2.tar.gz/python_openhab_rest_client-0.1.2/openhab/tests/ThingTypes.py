import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, ThingTypes

class ThingTypesTest:
    def __init__(self, client: OpenHABClient):
        self.discoveryAPI = ThingTypes(client)

    def testGetAllThingTypes(self, bindingID: str = None,):
        """Retrieve all thing types"""
        print("\n~~~~ Test #1 getAllThingTypes() ~~~~\n")

        try:
            allThingTypes = self.thingTypesAPI.getAllThingTypes(bindingID)
            print("All Thing Types:")
            print(json.dumps(allThingTypes, indent=4))
        except Exception as e:
            print(f"Error retrieving thing types: {e}")

    def testGetThingType(self, thingTypeUID: str):
        """Retrieve a specific thing type by UID"""
        print("\n~~~~ Test #2 getThingType(thingTypeUID) ~~~~\n")

        try:
            specificThingType = self.thingTypesAPI.getThingType(thingTypeUID)
            print("Thing Type Details:")
            print(json.dumps(specificThingType, indent=4))
        except Exception as e:
            print(f"Error retrieving thing type {thingTypeUID}: {e}")

