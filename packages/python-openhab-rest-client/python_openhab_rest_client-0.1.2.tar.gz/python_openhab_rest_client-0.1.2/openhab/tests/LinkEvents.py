import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, LinkEvents

class LinkEventsTest:
    def __init__(self, client: OpenHABClient):
        self.linkEvents = LinkEvents(client)

    def testItemChannelLinkAddedEvent(self, itemName: str, channelUID: str):
        """ Test the ItemChannelLinkAddedEvent method """
        print("\n~~~~ Test #1: ItemChannelLinkAddedEvent() ~~~~\n")
        
        try:
            response = self.linkEvents.ItemChannelLinkAddedEvent(itemName, channelUID)
            print(f"ItemChannelLinkAddedEvent response: {response}")
        except Exception as e:
            print(f"Error in ItemChannelLinkAddedEvent: {e}")

    def testItemChannelLinkRemovedEvent(self, itemName: str, channelUID: str):
        """ Test the ItemChannelLinkRemovedEvent method """
        print("\n~~~~ Test #2: ItemChannelLinkRemovedEvent() ~~~~\n")
        
        try:
            response = self.linkEvents.ItemChannelLinkRemovedEvent(itemName, channelUID)
            print(f"ItemChannelLinkRemovedEvent response: {response}")
        except Exception as e:
            print(f"Error in ItemChannelLinkRemovedEvent: {e}")
