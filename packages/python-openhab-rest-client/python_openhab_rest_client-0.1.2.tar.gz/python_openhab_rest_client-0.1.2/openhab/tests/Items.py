import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Items

class ItemsTest:
    def __init__(self, client: OpenHABClient):
        self.itemsAPI = Items(client)

    # Test fetching all items
    def testGetAllItems(self):
        print("\n~~~~ Test #1: getAllItems() ~~~~\n")

        try:
            allItems = self.itemsAPI.getAllItems()
            print("All Items:", allItems)
        except Exception as e:
            print(f"Error fetching all items: {e}")

    # Test fetching a specific item
    def testGetItem(self, itemName: str):
        print("\n~~~~ Test #2: getItem() ~~~~\n")

        try:
            item = self.itemsAPI.getItem(itemName)
            print(f"Details for {itemName}:", item)
        except Exception as e:
            print(f"Error fetching item '{itemName}': {e}")

    # Test adding or updating a single item
    def testAddOrUpdateItem(self, itemName: str, itemData: dict):
        print("\n~~~~ Test #3: addOrUpdateItem() ~~~~\n")

        try:
            self.itemsAPI.addOrUpdateItem(itemName, itemData)
            print(f"Item '{itemName}' added or updated.")
        except Exception as e:
            print(f"Error adding or updating item '{itemName}': {e}")

    # Test adding or updating multiple items
    def testAddOrUpdateItems(self, items: list):
        print("\n~~~~ Test #4: addOrUpdateItems() ~~~~\n")

        try:
            self.itemsAPI.addOrUpdateItems(items)
            print("Multiple items added or updated.")
        except Exception as e:
            print(f"Error adding or updating multiple items: {e}")

    # Test sending a command to an item
    def testSendCommand(self, itemName: str, command: str):
        print("\n~~~~ Test #5: sendCommand() ~~~~\n")

        try:
            self.itemsAPI.sendCommand(itemName, command)
            print(f"Command '{command}' sent to '{itemName}'.")
        except Exception as e:
            print(f"Error sending command to '{itemName}': {e}")

    # Test updating the state of an item
    def testUpdateItemState(self, itemName: str, state: str):
        print("\n~~~~ Test #6: updateItemState() ~~~~\n")

        try:
            self.itemsAPI.updateItemState(itemName, state)
            print(f"State of '{itemName}' updated to '{state}'.")
        except Exception as e:
            print(f"Error updating state of '{itemName}': {e}")

    # Test fetching the state of an item
    def testGetItemState(self, itemName: str):
        print("\n~~~~ Test #7: getItemState() ~~~~\n")

        try:
            state = self.itemsAPI.getItemState(itemName)
            print(f"State of '{itemName}':", state)
        except Exception as e:
            print(f"Error fetching state of '{itemName}': {e}")

    # Test deleting an item
    def testDeleteItem(self, itemName: str):
        print("\n~~~~ Test #8: deleteItem() ~~~~\n")

        try:
            self.itemsAPI.deleteItem(itemName)
            print(f"Item '{itemName}' deleted.")
        except Exception as e:
            print(f"Error deleting item '{itemName}': {e}")

    # Test adding a group member
    def testAddGroupMember(self, groupName: str, itemName: str):
        print("\n~~~~ Test #9: addGroupMember() ~~~~\n")

        try:
            self.itemsAPI.addGroupMember(groupName, itemName)
            print(f"Item '{itemName}' added to group '{groupName}'.")
        except Exception as e:
            print(f"Error adding item '{itemName}' to group '{groupName}': {e}")

    # Test removing a group member
    def testRemoveGroupMember(self, groupName: str, itemName: str):
        print("\n~~~~ Test #10: removeGroupMember() ~~~~\n")

        try:
            self.itemsAPI.removeGroupMember(groupName, itemName)
            print(f"Item '{itemName}' removed from group '{groupName}'.")
        except Exception as e:
            print(f"Error removing item '{itemName}' from group '{groupName}': {e}")

    # Test adding metadata to an item
    def testAddMetadata(self, itemName: str, namespace: str, metadata: dict):
        print("\n~~~~ Test #11: addMetadata() ~~~~\n")

        try:
            self.itemsAPI.addMetadata(itemName, namespace, metadata)
            print(f"Metadata added to '{itemName}' in namespace '{namespace}'.")
        except Exception as e:
            print(f"Error adding metadata to '{itemName}': {e}")

    # Test removing metadata from an item
    def testRemoveMetadata(self, itemName: str, namespace: str):
        print("\n~~~~ Test #12: removeMetadata() ~~~~\n")

        try:
            self.itemsAPI.removeMetadata(itemName, namespace)
            print(f"Metadata removed from '{itemName}' in namespace '{namespace}'.")
        except Exception as e:
            print(f"Error removing metadata from '{itemName}': {e}")

    # Test fetching metadata namespaces of an item
    def testGetMetadataNamespaces(self, itemName: str):
        print("\n~~~~ Test #13: getMetadataNamespaces() ~~~~\n")

        try:
            namespaces = self.itemsAPI.getMetadataNamespaces(itemName)
            print(f"Metadata namespaces for '{itemName}':", namespaces)
        except Exception as e:
            print(f"Error fetching metadata namespaces for '{itemName}': {e}")

    # Test purging orphaned metadata
    def testPurgeOrphanedMetadata(self):
        print("\n~~~~ Test #14: purgeOrphanedMetadata() ~~~~\n")

        try:
            self.itemsAPI.purgeOrphanedMetadata()
            print("Orphaned metadata purged.")
        except Exception as e:
            print(f"Error purging orphaned metadata: {e}")
