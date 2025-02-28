import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Actions

class ActionsTest:
    def __init__(self, client: OpenHABClient):
        self.actionsAPI = Actions(client)

    # Test the endpoint to retrieve all Actions of a Thing
    def testGetAllActions(self, thingUID: str, language: str = None):
        print("\n~~~~ Test #1 getAllActions(thingUID) ~~~~\n")

        try:
            actions = self.actionsAPI.getAllActions(thingUID, language)

            if isinstance(actions, dict) and "error" in actions:
                print(f"Error retrieving actions: {actions['error']}")
            else:
                print("Available actions:")
                for action in actions:
                    print(f"Action UID: {action['actionUid']}, Label: {action['label']}")
        except Exception as e:
            print(f"Error retrieving actions: {e}")

    # Test the endpoint to execute an Action of a Thing
    def testExecuteAction(self, thingUID: str, actionUID: str, actionInputs: dict, language: str = None):
        print("\n~~~~ Test #2 executeAction(thingUID, actionUID, actionInputs) ~~~~\n")

        try:
            # Execute the action
            response = self.actionsAPI.executeAction(thingUID, actionUID, actionInputs, language)
            
            # Check the response type
            if isinstance(response, dict):
                print(f"Action response: {response}")
            else:
                print(f"Unexpected response type: {type(response)}")
        except Exception as e:
            print(f"Error executing action: {e}")
