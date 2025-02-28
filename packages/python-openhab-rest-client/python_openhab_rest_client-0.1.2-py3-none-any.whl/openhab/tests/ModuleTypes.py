import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, ModuleTypes

class ModuleTypesTest:
    def __init__(self, client: OpenHABClient):
        self.moduleTypesAPI = ModuleTypes(client)

    def testGetAllModuleTypes(self, tags=None, typeFilter=None, language: str = None):
        """ Test retrieving all module types """
        print("\n~~~~ Test #1: getModuleTypes() ~~~~\n")
        try:
            moduleTypes = self.moduleTypesAPI.getModuleTypes(tags, typeFilter, language)
            print("All module types:", moduleTypes)
        except Exception as e:
            print(f"Error retrieving module types: {e}")

    def testGetSingleModuleType(self, moduleTypeUID: str, language: str = None):
        """ Test retrieving a specific module type """
        print("\n~~~~ Test #2: getModuleType(moduleTypeUID) ~~~~\n")
        try:
            moduleType = self.moduleTypesAPI.getModuleType(moduleTypeUID, language)
            print(f"Module type {moduleTypeUID}:", moduleType)
        except Exception as e:
            print(f"Error retrieving module type {moduleTypeUID}: {e}")

