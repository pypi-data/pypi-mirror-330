import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ChannelEvents

class ChannelEventsTest:
    def __init__(self, client: OpenHABClient):
        self.channelEvents = ChannelEvents(client)

    # Test the event for channel description change
    def testChannelDescriptionChangedEvent(self, channelUID: str = "*"):
        print("\n~~~~ Test #1: ChannelDescriptionChangedEvent() ~~~~\n")

        try:
            response = self.channelEvents.ChannelDescriptionChangedEvent(channelUID)
            print(response)
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test the event for channel triggered
    def testChannelTriggeredEvent(self, channelUID: str = "*"):
        print("\n~~~~ Test #2: ChannelTriggeredEvent() ~~~~\n")

        try:
            response = self.channelEvents.ChannelTriggeredEvent(channelUID)
            print(response)
        except Exception as e:
            print(f"Error executing action: {e}")
