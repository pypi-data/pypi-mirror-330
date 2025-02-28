import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Events

class EventsTest:
    def __init__(self, client: OpenHABClient):
        self.eventsAPI = Events(client)

    # Test retrieving all events
    def testGetAllEvents(self, topics: str = None):
        print("\n~~~~ Test #1: getAllEvents() ~~~~\n")

        try:
            events = self.eventsAPI.getAllEvents(topics)
            print("(Filtered) Events:", events)
        except ValueError as e:
            print("Error trying to retrieve Events:", e)

    # Test initiating new state tracker connection
    def testInitiateStateTracker(self):
        print("\n~~~~ Test #2: initiateStateTracker() ~~~~\n")

        try:
            connectionIDResponse = self.eventsAPI.initiateStateTracker()
            print("New Connection ID:", connectionIDResponse)
        except Exception as e:
            print("Error starting the state tracker connection:", e)

        connectionID = None
        for line in connectionIDResponse.iter_lines():
            if line.startswith(b"data: "):  # search line with ID
                connectionID = line.decode().split("data: ")[1].strip()
                break  # Read the first line (data)

        print("Found Connection ID:", connectionID)
        return connectionID

    # Test updating connection
    def testUpdateSSEConnectionItems(self, connectionID: str, items: list):
        print("\n~~~~ Test #3: updateSSEConnectionItems(connectionID, items) ~~~~\n")

        try:
            result = self.eventsAPI.updateSSEConnectionItems(connectionID=connectionID, items=items)
            print(result)
        except ValueError as e:
            print("Error updating the connection:", e)
