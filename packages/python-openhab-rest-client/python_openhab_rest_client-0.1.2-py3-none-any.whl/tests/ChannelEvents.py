import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient
from openhab.tests import ChannelEventsTest

if __name__ == "__main__":
    # Initialize OpenHAB client (replace with your OpenHAB URL and authentication details)
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    channelEventsTest = ChannelEventsTest(client)

    # Run all tests
    channelEventsTest.testChannelDescriptionChangedEvent()   # Test #1
    channelEventsTest.testChannelTriggeredEvent()            # Test #2
