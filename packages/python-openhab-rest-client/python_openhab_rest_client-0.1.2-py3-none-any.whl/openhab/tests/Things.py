import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Things

class ThingsTest:
    def __init__(self, client: OpenHABClient):
        self.thingsAPI = Things(client)

    def testGetAllThings(self):
        """Retrieve all Things"""
        print("\n~~~~ Test #1 getAllThings() ~~~~\n")

        try:
            allThings = self.thingsAPI.getAllThings()
            print(json.dumps(allThings, indent=4))
        except Exception as e:
            print(f"Error retrieving all Things: {e}")

    def testGetThingByUID(self, thingUID: str):
        """Retrieve details for a specific Thing"""
        print("\n~~~~ Test #2 getThingByUID(thingUID) ~~~~\n")

        try:
            thing = self.thingsAPI.getThingByUID(thingUID)
            print(json.dumps(thing, indent=4))
        except Exception as e:
            print(f"Error retrieving Thing {thingUID}: {e}")

    def testCreateThing(self, newThing: dict):
        """Create a new Thing"""
        print("\n~~~~ Test #3 createThing(newThing) ~~~~\n")

        try:
            response = self.thingsAPI.createThing(newThing)
            print("Thing created:", json.dumps(response, indent=4))
        except Exception as e:
            print(f"Error creating Thing: {e}")

    def testUpdateThing(self, thingUID: str, updatedData: dict):
        """Update a Thing"""
        print("\n~~~~ Test #4 updateThing(thingUID, updatedData) ~~~~\n")

        try:
            self.thingsAPI.updateThing(thingUID, updatedData)
            print(f"Thing {thingUID} updated successfully.")
        except Exception as e:
            print(f"Error updating Thing {thingUID}: {e}")

    def testDeleteThing(self, thingUID: str):
        """Delete a Thing"""
        print("\n~~~~ Test #5 deleteThing(thingUID) ~~~~\n")
        try:
            self.thingsAPI.deleteThing(thingUID, force=True)
            print(f"Thing {thingUID} deleted successfully.")
        except Exception as e:
            print(f"Error deleting Thing {thingUID}: {e}")

    def testGetThingStatus(self, thingUID: str):
        """Retrieve the status of a Thing"""
        print("\n~~~~ Test #6 getThingStatus(thingUID) ~~~~\n")

        try:
            status = self.thingsAPI.getThingStatus(thingUID)
            print(f"Status of Thing {thingUID}: {status}")
        except Exception as e:
            print(f"Error fetching status of Thing {thingUID}: {e}")

    def testEnableThing(self, thingUID: str, enabled: bool):
        """Enable or disable a Thing"""
        print("\n~~~~ Test #7 enableThing(thingUID, enabled) ~~~~\n")

        try:
            response = self.thingsAPI.enableThing(thingUID, enabled)
            print(f"Thing {thingUID} enabled: {response}")
        except Exception as e:
            print(f"Error enabling/disabling Thing {thingUID}: {e}")
