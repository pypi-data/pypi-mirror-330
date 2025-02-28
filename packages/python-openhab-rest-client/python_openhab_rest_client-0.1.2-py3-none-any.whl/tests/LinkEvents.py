import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient
from openhab.tests import LinkEventsTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    linkEventsTest = LinkEventsTest(client)

    # Test variables
    itemName = "*"
    channelUID = "*"

    # Run tests
    linkEventsTest.testItemChannelLinkAddedEvent(itemName, channelUID)     # Test #1
    linkEventsTest.testItemChannelLinkRemovedEvent(itemName, channelUID)   # Test #2
