import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient
from openhab.tests import ChannelTypesTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    channelTypesTest = ChannelTypesTest(client)

    # Define test variables
    language = "en"
    prefix = "mqtt"
    channelTypeUID = "mqtt:trigger"

    # Run all tests
    channelTypesTest.testGetAllChannelTypes(language)                   # Test #1
    channelTypesTest.testGetAllChannelTypes(language, prefix)           # Test #1b
    channelTypesTest.testGetChannelTypeByUID(channelTypeUID, language)  # Test #2
    channelTypesTest.testGetLinkableItemTypes(channelTypeUID)           # Test #3
