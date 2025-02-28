import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ConfigDescriptions

class ConfigDescriptionsTest:
    def __init__(self, client: OpenHABClient):
        self.configDescriptionsAPI = ConfigDescriptions(client)

    # Test fetching all configuration descriptions
    def testGetAllConfigDescriptions(self, language: str = None, scheme: str = None):
        print("\n~~~~ Test #1: getAllConfigDescriptions() ~~~~\n")

        try:
            response = self.configDescriptionsAPI.getAllConfigDescriptions(language=language, scheme=scheme)
            print("All Configuration Descriptions:", response)
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test fetching a specific configuration description by URI
    def testGetConfigDescriptionByURI(self, uri: str, language: str = None):
        print("\n~~~~ Test #2: getConfigDescriptionByURI() ~~~~\n")

        try:
            response = self.configDescriptionsAPI.getConfigDescriptionByURI(uri=uri, language=language)
            print(f"Configuration Description for URI '{uri}':", response)
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
