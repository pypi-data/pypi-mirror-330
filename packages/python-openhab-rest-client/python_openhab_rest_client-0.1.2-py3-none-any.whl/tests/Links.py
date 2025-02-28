import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import LinksTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    linksTest = LinksTest(client)

    # Test variables
    itemName = "Sunrise_Time"
    channelUID = "astro:sun:b54938fe5crise#start"

    # Run tests
    linksTest.testGetAllLinks()                                   # Test#1
    linksTest.testGetIndividualLink(itemName, channelUID)       # Test#2
    linksTest.testUnlinkItemFromChannel(itemName, channelUID)   # Test#3
    linksTest.testLinkItemToChannel(itemName, channelUID)       # Test#4
    linksTest.testGetOrphanLinks()                                # Test#5
    linksTest.testPurgeUnusedLinks()                              # Test#6
