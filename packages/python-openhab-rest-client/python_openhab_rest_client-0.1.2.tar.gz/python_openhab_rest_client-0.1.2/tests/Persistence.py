import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import PersistenceTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    persistenceTest = PersistenceTest(client)

    # Test variables
    serviceID = "mapdb"
    itemName = "TemperatureSensor1"
    testConfig = {"retention": "30d"}
    startTime = "2025-01-01T00:00:00.000Z"
    endTime = "2025-01-31T23:59:59.999Z"
    testTime = "2025-01-27T15:30:00.000Z"
    testState = "22.5"

    # Run tests
    persistenceTest.testGetAllPersistenceServices()                                           # Test #1
    persistenceTest.testGetServiceConfiguration(serviceID)                                 # Test #2
    persistenceTest.testSetServiceConfiguration(serviceID, testConfig)                    # Test #3
    persistenceTest.testDeleteServiceConfiguration(serviceID)                              # Test #4
    persistenceTest.testGetItemsForService(serviceID)                                      # Test #5
    persistenceTest.testGetItemPersistenceData(serviceID, itemName, startTime, endTime) # Test #6
    persistenceTest.testStoreItemData(serviceID, itemName, testTime, testState)         # Test #7
    persistenceTest.testDeleteItemData(serviceID, itemName, startTime, endTime)         # Test #8