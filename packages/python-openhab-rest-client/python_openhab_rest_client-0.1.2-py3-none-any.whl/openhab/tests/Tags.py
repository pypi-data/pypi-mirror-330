import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Tags

class TagsTest:
    def __init__(self, client: OpenHABClient):
        self.tagsAPI = Tags(client)

    def testGetTags(self):
        """Retrieve all tags"""
        print("\n~~~~ Test #1 getTags() ~~~~\n")

        try:
            allTags = self.tagsAPI.getTags()
            print(json.dumps(allTags, indent=4))
        except Exception as e:
            print(f"Error retrieving tags: {e}")

    def testCreateTag(self, tagData: dict):
        """Create a new tag"""
        print("\n~~~~ Test #2 createTag(tagData) ~~~~\n")

        try:
            response = self.tagsAPI.createTag(tagData)
            print("Tag created:", json.dumps(response, indent=4))
        except Exception as e:
            print(f"Error creating tag: {e}")

    def testGetTag(self, tagID: str):
        """Retrieve details for a specific tag"""
        print("\n~~~~ Test #3 getTag(tagID) ~~~~\n")

        try:
            tagDetails = self.tagsAPI.getTag(tagID)
            print(json.dumps(tagDetails, indent=4))
        except Exception as e:
            print(f"Error retrieving tag {tagID}: {e}")

    def testUpdateTag(self, tagID: str, updatedTagData: dict):
        """Update a tag"""
        print("\n~~~~ Test #4 updateTag(tagID) ~~~~\n")

        try:
            self.tagsAPI.updateTag(tagID, updatedTagData)
            print(f"Tag {tagID} updated successfully.")
        except Exception as e:
            print(f"Error updating tag {tagID}: {e}")

    def testDeleteTag(self, tagID: str):
        """Delete a tag"""
        print("\n~~~~ Test #5 deleteTag(tagID) ~~~~\n")

        try:
            self.tagsAPI.deleteTag(tagID)
            print(f"Tag {tagID} deleted successfully.")
        except Exception as e:
            print(f"Error deleting tag {tagID}: {e}")
