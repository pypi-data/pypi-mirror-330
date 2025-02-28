import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import ThingEventsTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    thingEventsTest = ThingEventsTest(client)

    # Define event filter
    thingUID = "*"

    # Run tests
    thingEventsTest.testThingAddedEvent(thingUID)                # Test #1
    thingEventsTest.testThingRemovedEvent(thingUID)              # Test #2
    thingEventsTest.testThingUpdatedEvent(thingUID)              # Test #3
    thingEventsTest.testThingStatusInfoEvent(thingUID)           # Test #4
    thingEventsTest.testThingStatusInfoChangedEvent(thingUID)    # Test #5
