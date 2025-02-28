import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import UITest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    uiTest = UITest(client)

    # Example data
    namespace = "home"
    componentUID = "unique-button-uid"

    componentData = {
        "component": "Button",
        "config": {"label": "Turn On Light", "action": "turn_on"},
        "slots": {"slot1": [{"component": "Icon", "config": {"icon": "light"}}]},
        "uid": componentUID,
        "tags": ["button", "light-control"],
        "props": {
            "uri": "/control/light",
            "parameters": [{"name": "light", "label": "Light", "type": "TEXT", "required": True}]
        },
        "timestamp": "2025-01-27T15:37:35.741Z",
        "type": "button"
    }

    updatedComponentData = {
        "component": "Button",
        "config": {"label": "Turn Off Light", "action": "turn_off"},
        "uid": componentUID
    }

    # Execute test functions
    uiTest.testGetUIComponents(namespace)                                       # Test #1
    uiTest.testAddUIComponent(namespace, componentData)                         # Test #2
    uiTest.testGetUIComponent(namespace, componentUID)                          # Test #3
    uiTest.testUpdateUIComponent(namespace, componentUID, updatedComponentData) # Test #4
    uiTest.testDeleteUIComponent(namespace, componentUID)                       # Test #5
    uiTest.testGetUITiles()                                                     # Test #6
