import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Addons

class AddonsTest:
    def __init__(self, client: OpenHABClient):
        self.addonsAPI = Addons(client)

    # Test the endpoint to retrieve all add-ons
    def testGetAddons(self, language: str = None):
        print("\n~~~~ Test #1 getAddons() ~~~~\n")

        try:
            response = self.addonsAPI.getAddons(language)
            print("Response from getAddons:", json.dumps(response, indent=2))
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test the endpoint to retrieve a specific add-on
    def testGetAddon(self, addonID: str, language: str = None):
        print("\n~~~~ Test #2 getAddon(addonID) ~~~~\n")

        try:
            response = self.addonsAPI.getAddon(addonID, language)
            print(f"Response from getAddon for {addonID}:", json.dumps(response, indent=2))
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test the endpoint to install an add-on
    def testInstallAddon(self, addonID: str, language: str = None):
        print("\n~~~~ Test #3 installAddon(addonID) ~~~~\n")

        try:
            response = self.addonsAPI.installAddon(addonID, language)
            print(f"Response from installAddon for {addonID}:", json.dumps(response, indent=2))
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test the endpoint to uninstall an add-on
    def testUninstallAddon(self, addonID: str, language: str = None):
        print("\n~~~~ Test #4 uninstallAddon(addonID) ~~~~\n")

        try:
            response = self.addonsAPI.uninstallAddon(addonID, language)
            print(f"Response from uninstallAddon for {addonID}:", json.dumps(response, indent=2))
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test the endpoint to retrieve add-on types
    def testGetAddonTypes(self, language: str = None):
        print("\n~~~~ Test #5 getAddonTypes() ~~~~\n")

        try:
            response = self.addonsAPI.getAddonTypes(language)
            print("Response from getAddonTypes:", json.dumps(response, indent=2))
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test the endpoint to retrieve recommended add-ons
    def testGetAddonSuggestions(self, language: str = None):
        print("\n~~~~ Test #6 getAddonSuggestions() ~~~~\n")

        try:
            response = self.addonsAPI.getAddonSuggestions(language)
            print("Response from getAddonSuggestions:", json.dumps(response, indent=2))
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test the endpoint to retrieve add-on configuration
    def testGetAddonConfig(self, addonID: str):
        print("\n~~~~ Test #7 getAddonConfig(addonID) ~~~~\n")

        try:
            response = self.addonsAPI.getAddonConfig(addonID)
            print(f"Response from getAddonConfig for {addonID}:", json.dumps(response, indent=2))
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test the endpoint to update the add-on configuration
    def testUpdateAddonConfig(self, addonID: str, configData: dict):
        print("\n~~~~ Test #8 updateAddonConfig(addonID, configData) ~~~~\n")

        try:
            response = self.addonsAPI.updateAddonConfig(addonID, configData)
            print(f"Response from updateAddonConfig for {addonID}:", json.dumps(response, indent=2))
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test the endpoint to retrieve add-on services
    def testGetAddonServices(self, language: str = None):
        print("\n~~~~ Test #9 getAddonServices() ~~~~\n")

        try:
            response = self.addonsAPI.getAddonServices(language)
            print("Response from getAddonServices:", json.dumps(response, indent=2))
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test the endpoint to install an add-on from a URL
    def testInstallAddonFromUrl(self, url: str):
        print("\n~~~~ Test #10 installAddonFromUrl(url) ~~~~\n")

        try:
            response = self.addonsAPI.installAddonFromUrl(url)
            print(f"Response from installAddonFromUrl for URL {url}:", json.dumps(response, indent=2))
        except Exception as e:
            print(f"Error executing action: {e}")
