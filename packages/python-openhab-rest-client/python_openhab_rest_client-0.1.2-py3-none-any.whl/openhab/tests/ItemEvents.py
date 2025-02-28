import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ItemEvents

class ItemEventsTest:
    def __init__(self, client: OpenHABClient):
        self.itemEventsAPI = ItemEvents(client)

    # Test fetching a generic item event
    def testItemEvent(self):
        print("\n~~~~ Test #1: ItemEvent() ~~~~\n")

        try:
            response = self.itemEventsAPI.ItemEvent()
            print(response)
        except Exception as e:
            print(f"Error fetching ItemEvent: {e}")

    # Test fetching an item added event
    def testItemAddedEvent(self, itemName: str = "*"):
        print("\n~~~~ Test #2: ItemAddedEvent(itemName) ~~~~\n")

        try:
            response = self.itemEventsAPI.ItemAddedEvent(itemName)
            print(response)
        except Exception as e:
            print(f"Error fetching ItemAddedEvent: {e}")

    # Test fetching an item removed event
    def testItemRemovedEvent(self, itemName: str = "*"):
        print("\n~~~~ Test #3: ItemRemovedEvent(itemName) ~~~~\n")

        try:
            response = self.itemEventsAPI.ItemRemovedEvent(itemName)
            print(response)
        except Exception as e:
            print(f"Error fetching ItemRemovedEvent: {e}")

    # Test fetching an item updated event
    def testItemUpdatedEvent(self, itemName: str = "*"):
        print("\n~~~~ Test #4: ItemUpdatedEvent(itemName) ~~~~\n")

        try:
            response = self.itemEventsAPI.ItemUpdatedEvent(itemName)
            print(response)
        except Exception as e:
            print(f"Error fetching ItemUpdatedEvent: {e}")

    # Test fetching an item command event
    def testItemCommandEvent(self, itemName: str = "*"):
        print("\n~~~~ Test #5: ItemCommandEvent(itemName) ~~~~\n")

        try:
            response = self.itemEventsAPI.ItemCommandEvent(itemName)
            print(response)
        except Exception as e:
            print(f"Error fetching ItemCommandEvent: {e}")

    # Test fetching an item state event
    def testItemStateEvent(self, itemName: str = "*"):
        print("\n~~~~ Test #6: ItemStateEvent(itemName) ~~~~\n")

        try:
            response = self.itemEventsAPI.ItemStateEvent(itemName)
            print(response)
        except Exception as e:
            print(f"Error fetching ItemStateEvent: {e}")

    # Test fetching an item state predicted event
    def testItemStatePredictedEvent(self, itemName: str = "*"):
        print("\n~~~~ Test #7: ItemStatePredictedEvent(itemName) ~~~~\n")

        try:
            response = self.itemEventsAPI.ItemStatePredictedEvent(itemName)
            print(response)
        except Exception as e:
            print(f"Error fetching ItemStatePredictedEvent: {e}")

    # Test fetching an item state changed event
    def testItemStateChangedEvent(self, itemName: str = "*"):
        print("\n~~~~ Test #8: ItemStateChangedEvent(itemName) ~~~~\n")

        try:
            response = self.itemEventsAPI.ItemStateChangedEvent(itemName)
            print(response)
        except Exception as e:
            print(f"Error fetching ItemStateChangedEvent: {e}")

    # Test fetching a group item state changed event
    def testGroupItemStateChangedEvent(self, itemName: str = "*", memberName: str = "*"):
        print("\n~~~~ Test #9: GroupItemStateChangedEvent(itemName, memberName) ~~~~\n")

        try:
            response = self.itemEventsAPI.GroupItemStateChangedEvent(itemName, memberName)
            print(response)
        except Exception as e:
            print(f"Error fetching GroupItemStateChangedEvent: {e}")

    # Test processing ItemStateChangedEvent stream
    def testItemStateChangedEventStream(self):
        print("\n~~~~ Test #10: ItemStateChangedEvent Stream() ~~~~\n")

        try:
            response = self.itemEventsAPI.ItemStateChangedEvent()
            with response as events:
                for line in events.iter_lines():
                    line = line.decode()

                    if "data" in line:
                        line = line.replace("data: ", "")
                        try:
                            data = json.loads(line)
                            print(data)
                        except json.decoder.JSONDecodeError:
                            print("Event could not be converted to JSON")
        except Exception as e:
            print(f"Error processing ItemStateChangedEvent stream: {e}")
