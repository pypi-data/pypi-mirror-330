import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient
from openhab.tests import ItemsTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    itemsTest = ItemsTest(client)

    # Define test variables
    testItemName = "testSwitch"
    newItemData = {
        "type": "Switch",
        "name": "newSwitch",
        "label": "New Switch",
        "groupNames": ["Static"],
        "tags": ["SwitchTag"],
        "category": "Switch"
    }
    testMetadata = {
        "value": "metadata_value",
        "config": {
            "key1": "value1",
            "key2": "value2"
        }
    }
    
    # Run tests
    itemsTest.testGetAllItems()                                                   # Test#1
    itemsTest.testGetItem(testItemName)                                         # Test#2
    itemsTest.testAddOrUpdateItem("newSwitch", newItemData)                     # Test#3
    itemsTest.testAddOrUpdateItems([newItemData])                               # Test#4
    itemsTest.testSendCommand(testItemName, "ON")                               # Test#5
    itemsTest.testUpdateItemState("testNumber", "42")                           # Test#6
    itemsTest.testGetItemState(testItemName)                                    # Test#7
    itemsTest.testDeleteItem("newSwitch")                                       # Test#8
    itemsTest.testAddGroupMember("Static", "testNumber")                        # Test#9
    itemsTest.testRemoveGroupMember("Static", "testNumber")                     # Test#10
    itemsTest.testAddMetadata(testItemName, "exampleNamespace", testMetadata)   # Test#11
    itemsTest.testRemoveMetadata(testItemName, "exampleNamespace")              # Test#12
    itemsTest.testGetMetadataNamespaces(testItemName)                           # Test#13
    itemsTest.testPurgeOrphanedMetadata()                                         # Test#14
