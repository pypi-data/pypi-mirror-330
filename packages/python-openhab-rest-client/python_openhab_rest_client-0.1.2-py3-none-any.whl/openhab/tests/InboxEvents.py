import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, InboxEvents

class InboxEventsTest:
    def __init__(self, client: OpenHABClient):
        self.inboxEvents = InboxEvents(client)

    def testInboxAddedEvent(self, thingUID: str = "*"):
        print("\n~~~~ Test #1: InboxAddedEvent(thingUID) ~~~~\n")

        try:
            response = self.inboxEvents.InboxAddedEvent(thingUID)
            print(response)
        except Exception as e:
            print(f"Error executing action: {e}")

    def testInboxRemovedEvent(self, thingUID: str = "*"):
        print("\n~~~~ Test #2: InboxRemovedEvent(thingUID) ~~~~\n")

        try:
            response = self.inboxEvents.InboxRemovedEvent(thingUID)
            print(response)
        except Exception as e:
            print(f"Error executing action: {e}")

    def testInboxUpdatedEvent(self, thingUID: str = "*"):
        print("\n~~~~ Test #3: InboxUpdatedEvent(thingUID) ~~~~\n")

        try:
            response = self.inboxEvents.InboxUpdatedEvent(thingUID)
            print(response)
        except Exception as e:
            print(f"Error executing action: {e}")
