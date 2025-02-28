import sys
import os
import json
import time

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Links

class LinksTest:
    def __init__(self, client: OpenHABClient):
        self.linksAPI = Links(client)

    def testGetAllLinks(self):
        """ Test fetching all links """
        print("\n~~~~ Test #1: getAllLinks() ~~~~\n")

        try:
            allLinks = self.linksAPI.getAllLinks()
            print(json.dumps(allLinks, indent=2))
        except Exception as e:
            print(f"Error retrieving all links: {e}")

    def testGetIndividualLink(self, itemName: str, channelUID: str):
        """ Test fetching a specific link """
        print("\n~~~~ Test #2: getIndividualLink(itemName, channelUID) ~~~~\n")

        try:
            link = self.linksAPI.getIndividualLink(itemName, channelUID)
            print(json.dumps(link, indent=2))
        except Exception as e:
            print(f"Error retrieving link {itemName} -> {channelUID}: {e}")

    def testUnlinkItemFromChannel(self, itemName: str, channelUID: str):
        """ Test unlinking an item from a channel """
        print("\n~~~~ Test #3: unlinkItemFromChannel(itemName, channelUID) ~~~~\n")

        try:
            response = self.linksAPI.unlinkItemFromChannel(itemName, channelUID)
            print(f"Link removed: {response}")
            time.sleep(1)  # Small delay for API stability
        except Exception as e:
            print(f"Error unlinking {itemName} -> {channelUID}: {e}")

    def testLinkItemToChannel(self, itemName: str, channelUID: str, config: dict = {}):
        """ Test linking an item to a channel """
        print("\n~~~~ Test #4: linkItemToChannel(itemName, channelUID) ~~~~\n")

        try:
            response = self.linksAPI.linkItemToChannel(itemName, channelUID, config)
            print(f"Link created: {json.dumps(response, indent=2)}")
        except Exception as e:
            print(f"Error linking {itemName} -> {channelUID}: {e}")

    def testGetOrphanLinks(self):
        """ Test retrieving orphan links """
        print("\n~~~~ Test #5: getOrphanLinks() ~~~~\n")

        try:
            orphanLinks = self.linksAPI.getOrphanLinks()
            print(json.dumps(orphanLinks, indent=2))
        except Exception as e:
            print(f"Error retrieving orphan links: {e}")

    def testPurgeUnusedLinks(self):
        """ Test purging unused links """
        print("\n~~~~ Test #6: purgeUnusedLinks() ~~~~\n")

        try:
            response = self.linksAPI.purgeUnusedLinks()
            print(f"Unused links purged: {response}")
        except Exception as e:
            print(f"Error purging unused links: {e}")
