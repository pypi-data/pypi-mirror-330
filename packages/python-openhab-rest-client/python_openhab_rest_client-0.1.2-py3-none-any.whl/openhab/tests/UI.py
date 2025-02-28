import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, UI

class UITest:
    def __init__(self, client: OpenHABClient):
        self.uiAPI = UI(client)

    def testGetUIComponents(self, namespace: str):
        """Retrieve all UI components for a given namespace"""
        print("\n~~~~ Test #1: getUiComponents(namespace) ~~~~\n")

        try:
            components = self.uiAPI.getUIComponents(namespace)
            print(json.dumps(components, indent=4))
        except Exception as e:
            print(f"Error retrieving UI components for {namespace}: {e}")

    def testAddUIComponent(self, namespace: str, componentData: dict):
        """Add a new UI component"""
        print("\n~~~~ Test #2: addUiComponent(namespace, componentData) ~~~~\n")

        try:
            newComponent = self.uiAPI.addUIComponent(namespace, componentData)
            print(f"New UI component added:\n{json.dumps(newComponent, indent=4)}")
        except Exception as e:
            print(f"Error adding new UI component: {e}")

    def testGetUIComponent(self, namespace: str, componentUID: str):
        """Retrieve a specific UI component by UID"""
        print("\n~~~~ Test #3: getUiComponent(namespace, componentUID) ~~~~\n")

        try:
            component = self.uiAPI.getUIComponent(namespace, componentUID)
            print(json.dumps(component, indent=4))
        except Exception as e:
            print(f"Error retrieving UI component {componentUID}: {e}")

    def testUpdateUIComponent(self, namespace: str, componentUID: str, updatedComponentData: dict):
        """Update a UI component by UID"""
        print("\n~~~~ Test #4: updateUiComponent(namespace, componentUID) ~~~~\n")

        try:
            updatedComponent = self.uiAPI.updateUIComponent(namespace, componentUID, updatedComponentData)
            print(f"Updated UI component {componentUID}:\n{json.dumps(updatedComponent, indent=4)}")
        except Exception as e:
            print(f"Error updating UI component {componentUID}: {e}")

    def testDeleteUIComponent(self, namespace: str, componentUID: str):
        """Delete a UI component by UID"""
        print("\n~~~~ Test #5: deleteUiComponent(namespace, componentUID) ~~~~\n")

        try:
            self.uiAPI.deleteUiComponent(namespace, componentUID)
            print(f"UI component {componentUID} deleted successfully.")
        except Exception as e:
            print(f"Error deleting UI component {componentUID}: {e}")

    def testGetUITiles(self):
        """Retrieve all UI tiles"""
        print("\n~~~~ Test #6: getUiTiles() ~~~~\n")

        try:
            tiles = self.uiAPI.getUITiles()
            print(json.dumps(tiles, indent=4))
        except Exception as e:
            print(f"Error retrieving UI tiles: {e}")
