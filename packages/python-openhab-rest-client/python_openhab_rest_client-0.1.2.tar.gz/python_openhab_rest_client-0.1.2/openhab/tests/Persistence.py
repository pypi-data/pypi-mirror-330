import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Persistence

class PersistenceTest:
    def __init__(self, client: OpenHABClient):
        self.persistenceAPI = Persistence(client)

    def testGetAllPersistenceServices(self):
        """ Retrieve all available persistence services """
        print("\n~~~~ Test #1: getAllServices() ~~~~\n")

        try:
            services = self.persistenceAPI.getAllServices()
            print(json.dumps(services, indent=4))
        except Exception as e:
            print(f"Error retrieving persistence services: {e}")

    def testGetServiceConfiguration(self, serviceID: str):
        """ Retrieve the configuration of a specific persistence service """
        print("\n~~~~ Test #2: getServiceConfiguration(serviceID) ~~~~\n")

        try:
            config = self.persistenceAPI.getServiceConfiguration(serviceID)
            print(json.dumps(config, indent=4))
        except Exception as e:
            print(f"Error retrieving configuration for {serviceID}: {e}")

    def testSetServiceConfiguration(self, serviceID: str, newConfig: dict):
        """ Update the configuration of a persistence service """
        print("\n~~~~ Test #3: setServiceConfiguration(serviceID) ~~~~\n")

        try:
            updatedConfig = self.persistenceAPI.setServiceConfiguration(serviceID, newConfig)
            print(json.dumps(updatedConfig, indent=4))
        except Exception as e:
            print(f"Error updating configuration for {serviceID}: {e}")

    def testDeleteServiceConfiguration(self, serviceID: str):
        """ Delete the configuration of a persistence service """
        print("\n~~~~ Test #4: deleteServiceConfiguration(serviceID) ~~~~\n")

        try:
            response = self.persistenceAPI.deleteServiceConfiguration(serviceID)
            print(json.dumps(response, indent=4))
        except Exception as e:
            print(f"Error deleting configuration for {serviceID}: {e}")

    def testGetItemsForService(self, serviceID: str):
        """ Retrieve all items stored by a specific persistence service """
        print("\n~~~~ Test #5: getItemsForService(serviceID) ~~~~\n")

        try:
            items = self.persistenceAPI.getItemsForService(serviceID)
            print(json.dumps(items, indent=4))
        except Exception as e:
            print(f"Error retrieving items for service {serviceID}: {e}")

    def testGetItemPersistenceData(self, serviceID: str, itemName: str, startTime: str, endTime: str):
        """ Retrieve persistence data for a specific item """
        print("\n~~~~ Test #6: getItemPersistenceData(itemName) ~~~~\n")

        try:
            itemData = self.persistenceAPI.getItemPersistenceData(serviceID, itemName, startTime=startTime, endTime=endTime)
            print(json.dumps(itemData, indent=4))
        except Exception as e:
            print(f"Error retrieving persistence data for {itemName}: {e}")

    def testStoreItemData(self, serviceID: str, itemName: str, time: str, state: str):
        """ Store persistence data for a specific item """
        print("\n~~~~ Test #7: storeItemData(itemName) ~~~~\n")

        try:
            response = self.persistenceAPI.storeItemData(serviceID, itemName, time, state)
            print("Data successfully stored:", response)
        except Exception as e:
            print(f"Error storing data for {itemName}: {e}")

    def testDeleteItemData(self, serviceID: str, itemName: str, startTime: str, endTime: str):
        """ Delete persistence data for a specific item """
        print("\n~~~~ Test #8: deleteItemData(itemName) ~~~~\n")

        try:
            response = self.persistenceAPI.deleteItemData(serviceID, itemName, startTime, endTime)
            print(json.dumps(response, indent=4))
        except Exception as e:
            print(f"Error deleting persistence data for {itemName}: {e}")
