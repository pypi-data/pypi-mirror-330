import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import ServicesTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    servicesTest = ServicesTest(client)

    # Example service ID
    serviceID = "org.openhab.i18n"
    
    # Example new configuration
    newConfig = {
        "enabled": True,
        "setting1": "newValue1"
    }

    # Execute test functions
    servicesTest.testGetAllServices()                             # Test #1
    servicesTest.testGetService(serviceID)                      # Test #2
    servicesTest.testGetServiceConfig(serviceID)                # Test #3
    servicesTest.testUpdateServiceConfig(serviceID, newConfig)  # Test #4
    servicesTest.testDeleteServiceConfig(serviceID)             # Test #5
    servicesTest.testGetServiceContexts(serviceID)              # Test #6
