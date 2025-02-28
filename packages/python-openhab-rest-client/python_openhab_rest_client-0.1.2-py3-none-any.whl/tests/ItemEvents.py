import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient
from openhab.tests import ItemEventsTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    itemEventsTest = ItemEventsTest(client)

    # Variables
    itemName = "*"
    memberName = "*"

    # Run all tests
    itemEventsTest.testItemEvent()                                          # Test #1
    itemEventsTest.testItemAddedEvent(itemName)                             # Test #2
    itemEventsTest.testItemRemovedEvent(itemName)                           # Test #3
    itemEventsTest.testItemUpdatedEvent(itemName)                           # Test #4
    itemEventsTest.testItemCommandEvent(itemName)                           # Test #5
    itemEventsTest.testItemStateEvent(itemName)                             # Test #6
    itemEventsTest.testItemStatePredictedEvent(itemName)                    # Test #7
    itemEventsTest.testItemStateChangedEvent(itemName)                      # Test #8
    itemEventsTest.testGroupItemStateChangedEvent(itemName, memberName)     # Test #9
    itemEventsTest.testItemStateChangedEventStream()                        # Test #10
