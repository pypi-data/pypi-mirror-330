import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient
from openhab.tests import EventsTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    eventsTest = EventsTest(client)

    # Variables
    topics = "topic1,topic2"
    items = ["item1", "item2"]

    # Run all tests
    eventsTest.testGetAllEvents()                                  # Test #1
    eventsTest.testGetAllEvents(topics)                          # Test #1b
    connectionID = eventsTest.testInitiateStateTracker()           # Test #2
    eventsTest.testUpdateSSEConnectionItems(connectionID, items) # Test #3
