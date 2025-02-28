import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import ThingTypesTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    thingTypesTest = ThingTypesTest(client)

    # Example thing type UID
    thingTypeUID = "mqtt:homeassistant"

    # Execute test functions
    thingTypesTest.testGetAllThingTypes()       # Test #1
    thingTypesTest.testGetThingType(thingTypeUID)  # Test #2
