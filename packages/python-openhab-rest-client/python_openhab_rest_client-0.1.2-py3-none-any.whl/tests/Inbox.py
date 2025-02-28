import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient
from openhab.tests import InboxTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    inboxTest = InboxTest(client)

    # Define test variables
    thingUIDToRemove = "avmfritz:fritzbox:192_168_3_1"
    thingUIDToApprove = "avmfritz:fritzbox:192_168_2_1"
    thingLabel = "My FritzBox Router"
    thingUIDToIgnore = "avmfritz:fritzbox:192_168_2_1"
    thingUIDToUnignore = "avmfritz:fritzbox:192_168_2_1"

    # Run all tests
    inboxTest.testGetAllDiscoveredThings()                              # Test #1
    inboxTest.testRemoveDiscoveryResult(thingUIDToRemove)               # Test #2
    inboxTest.testApproveDiscoveryResult(thingUIDToApprove, thingLabel) # Test #3
    inboxTest.testIgnoreDiscoveryResult(thingUIDToIgnore)               # Test #4
    inboxTest.testUnignoreDiscoveryResult(thingUIDToUnignore)           # Test #5
