import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Inbox

class InboxTest:
    def __init__(self, client: OpenHABClient):
        self.inboxAPI = Inbox(client)

    # Test fetching all discovered things
    def testGetAllDiscoveredThings(self, includeIgnored: bool = True):
        print("\n~~~~ Test #1: getAllDiscoveredThings() ~~~~\n")

        try:
            response = self.inboxAPI.getAllDiscoveredThings(includeIgnored)
            print("Discovered Things:", response)
        except Exception as e:
            print(f"Error retrieving discovered things: {e}")

    # Test removing a discovery result
    def testRemoveDiscoveryResult(self, thingUID: str):
        print("\n~~~~ Test #2: removeDiscoveryResult(thingUID) ~~~~\n")

        try:
            response = self.inboxAPI.removeDiscoveryResult(thingUID)
            print(f"Discovery result '{thingUID}' removed:", response)
        except Exception as e:
            print(f"Error removing discovery result '{thingUID}': {e}")

    # Test approving a discovered thing
    def testApproveDiscoveryResult(self, thingUID: str, thingLabel: str, newThingID: str = None, language: str = None):
        print("\n~~~~ Test #3: approveDiscoveryResult(thingUID, thingLabel) ~~~~\n")

        try:
            response = self.inboxAPI.approveDiscoveryResult(thingUID, thingLabel, newThingID, language)
            print(f"Discovery result '{thingUID}' approved:", response)
        except Exception as e:
            print(f"Error approving discovery result '{thingUID}': {e}")

    # Test ignoring a discovery result
    def testIgnoreDiscoveryResult(self, thingUID: str):
        print("\n~~~~ Test #4: ignoreDiscoveryResult(thingUID) ~~~~\n")

        try:
            response = self.inboxAPI.ignoreDiscoveryResult(thingUID)
            print(f"Discovery result '{thingUID}' ignored:", response)
        except Exception as e:
            print(f"Error ignoring discovery result '{thingUID}': {e}")

    # Test unignoring a discovery result
    def testUnignoreDiscoveryResult(self, thingUID: str):
        print("\n~~~~ Test #5: unignoreDiscoveryResult(thingUID) ~~~~\n")

        try:
            response = self.inboxAPI.unignoreDiscoveryResult(thingUID)
            print(f"Discovery result '{thingUID}' unignored:", response)
        except Exception as e:
            print(f"Error unignoring discovery result '{thingUID}': {e}")
