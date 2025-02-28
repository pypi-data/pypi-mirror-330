import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, ThingEvents

class ThingEventsTest:
    def __init__(self, client: OpenHABClient):
        self.discoveryAPI = ThingEvents(client)

    def testThingAddedEvent(self, thingUID: str):
        """Test fetching ThingAddedEvent"""
        print("\n~~~~ Test #1: ThingAddedEvent(thingUID) ~~~~\n")

        try:
            event = selfthingEventsAPI.ThingAddedEvent(thingUID)
            print(event)
        except Exception as e:
            print(f"Error fetching ThingAddedEvent: {e}")

    def testThingRemovedEvent(self, thingUID: str):
        """Test fetching ThingRemovedEvent"""
        print("\n~~~~ Test #2: ThingRemovedEvent(thingUID) ~~~~\n")

        try:
            event = self.thingEventsAPI.ThingRemovedEvent(thingUID)
            print(event)
        except Exception as e:
            print(f"Error fetching ThingRemovedEvent: {e}")

    def testThingUpdatedEvent(self, thingUID: str):
        """Test fetching ThingUpdatedEvent"""
        print("\n~~~~ Test #3: ThingUpdatedEvent(thingUID) ~~~~\n")

        try:
            event = self.thingEventsAPI.ThingUpdatedEvent(thingUID)
            print(event)
        except Exception as e:
            print(f"Error fetching ThingUpdatedEvent: {e}")

    def testThingStatusInfoEvent(self, thingUID: str):
        """Test fetching ThingStatusInfoEvent"""
        print("\n~~~~ Test #4: ThingStatusInfoEvent(thingUID) ~~~~\n")

        try:
            event = self.thingEventsAPI.ThingStatusInfoEvent(thingUID)
            print(event)
        except Exception as e:
            print(f"Error fetching ThingStatusInfoEvent: {e}")

    def testThingStatusInfoChangedEvent(self, thingUID: str):
        """Test fetching ThingStatusInfoChangedEvent"""
        print("\n~~~~ Test #5: ThingStatusInfoChangedEvent(thingUID) ~~~~\n")

        try:
            event = self.thingEventsAPI.ThingStatusInfoChangedEvent(thingUID)
            print(event)
        except Exception as e:
            print(f"Error fetching ThingStatusInfoChangedEvent: {e}")
