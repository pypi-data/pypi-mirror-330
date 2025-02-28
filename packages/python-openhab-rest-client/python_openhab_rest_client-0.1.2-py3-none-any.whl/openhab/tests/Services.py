import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Services

class ServicesTest:
    def __init__(self, client: OpenHABClient):
        self.servicesAPI = Services(client)

    def testGetAllServices(self, language: str = "de"):
        """Retrieve all services"""
        print("\n~~~~ Test #1 getServices() ~~~~\n")

        try:
            services = self.servicesAPI.getServices(language=language)
            print(json.dumps(services, indent=4))
        except Exception as e:
            print(f"Error retrieving services: {e}")

    def testGetService(self, serviceID: str):
        """Retrieve a specific service"""
        print("\n~~~~ Test #2 getService(serviceID) ~~~~\n")

        try:
            service = self.servicesAPI.getService(serviceID)
            print(json.dumps(service, indent=4))
        except Exception as e:
            print(f"Error retrieving service {serviceID}: {e}")

    def testGetServiceConfig(self, serviceID: str):
        """Retrieve the configuration of a service"""
        print("\n~~~~ Test #3 getServiceConfig(serviceID) ~~~~\n")

        try:
            config = self.servicesAPI.getServiceConfig(serviceID)
            print(json.dumps(config, indent=4))
        except Exception as e:
            print(f"Error retrieving configuration for {serviceID}: {e}")

    def testUpdateServiceConfig(self, serviceID: str, newConfig: dict):
        """Update the configuration of a service"""
        print("\n~~~~ Test #4 updateServiceConfig(serviceID) ~~~~\n")

        try:
            old_config = self.servicesAPI.updateServiceConfig(serviceID, newConfig)
            print("Old Configuration:", json.dumps(old_config, indent=4))
        except Exception as e:
            print(f"Error updating configuration for {serviceID}: {e}")

    def testDeleteServiceConfig(self, serviceID: str):
        """Delete the configuration of a service"""
        print("\n~~~~ Test #5 deleteServiceConfig(serviceID) ~~~~\n")

        try:
            deleted_config = self.servicesAPI.deleteServiceConfig(serviceID)
            print("Deleted Configuration:", json.dumps(deleted_config, indent=4))
        except Exception as e:
            print(f"Error deleting configuration for {serviceID}: {e}")

    def testGetServiceContexts(self, serviceID: str):
        """Retrieve all contexts of a service"""
        print("\n~~~~ Test #6 getServiceContexts(serviceID) ~~~~\n")

        try:
            contexts = self.servicesAPI.getServiceContexts(serviceID)
            print(json.dumps(contexts, indent=4))
        except Exception as e:
            print(f"Error retrieving contexts for {serviceID}: {e}")
