import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient
from openhab.tests import AddonsTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    addonsTest = AddonsTest(client)

    addonID = "binding-astro"

    configData = {
        "latitude": 52.52,  # Berlin
        "longitude": 13.405, 
        "interval": 300  # Update every 5 minutes
    }
    
    # Replace this URL with a valid OpenHAB add-on URL
    url = "https://repo1.maven.org/maven2/org/smarthomej/addons/bundles/org.smarthomej.binding.amazonechocontrol/4.2.0/org.smarthomej.binding.amazonechocontrol-4.2.0.kar"
    
    # Run all tests
    addonsTest.testGetAddons()                                # Test #1
    addonsTest.testGetAddon(addonID)                        # Test #2
    addonsTest.testInstallAddon(addonID)                    # Test #3
    addonsTest.testUninstallAddon(addonID)                  # Test #4
    addonsTest.testGetAddonTypes()                            # Test #5
    addonsTest.testGetAddonSuggestions()                      # Test #6
    addonsTest.testGetAddonConfig(addonID)                  # Test #7
    addonsTest.testUpdateAddonConfig(addonID, configData)   # Test #8
    addonsTest.testGetAddonServices()                         # Test #9
    addonsTest.testInstallAddonFromUrl(url)                 # Test #10
