import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import TagsTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    tagsTest = TagsTest(client)

    # Example tag data
    newTagData = {
        "uid": "CustomTag",
        "name": "CustomTag",
        "label": "My Custom Tag",
        "description": "This is a custom tag",
        "synonyms": ["Custom", "Tag"],
        "editable": True
    }

    # Example tag ID
    tagID = "Property_Voltage"

    # Execute test functions
    tagsTest.testGetTags()                                                  # Test #1
    tagsTest.testCreateTag(newTagData)                                      # Test #2
    tagsTest.testGetTag(tagID)                                              # Test #3
    tagsTest.testUpdateTag(tagID, {"id": tagID, "label": "Updated Tag"})    # Test #4
    tagsTest.testDeleteTag(tagID)                                           # Test #5
