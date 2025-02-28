import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import ThingsTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    thingsTest = ThingsTest(client)

    # Example Thing data
    thingUID = "mqtt:topic:mybroker:newthing"
    newThing = {
        "UID": "mqtt:topic:mybroker:newthing",
        "label": "New MQTT Thing",
        "thingTypeUID": "mqtt:topic",
        "bridgeUID": "mqtt:broker:mybroker",
        "configuration": {},
        "channels": []
    }
    updatedData = {"label": "Updated MQTT Thing"}

    # Execute test functions
    thingsTest.testGetAllThings()                         # Test #1
    thingsTest.testGetThingByUID(thingUID)              # Test #2
    thingsTest.testCreateThing(newThing)                # Test #3
    thingsTest.testUpdateThing(thingUID, updatedData)   # Test #4
    thingsTest.testDeleteThing(thingUID)                # Test #5
    thingsTest.testGetThingStatus(thingUID)             # Test #6
    thingsTest.testEnableThing(thingUID, enabled=True)  # Test #7
