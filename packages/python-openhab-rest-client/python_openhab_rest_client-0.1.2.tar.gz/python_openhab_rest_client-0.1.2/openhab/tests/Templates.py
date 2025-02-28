import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Templates

class TemplatesTest:
    def __init__(self, client: OpenHABClient):
        self.templatesAPI = Templates(client)

    def testGetAllTemplates(self):
        """Retrieve all templates"""
        print("\n~~~~ Test #1 getAllTemplates() ~~~~\n")

        try:
            allTemplates = self.templatesAPI.getAllTemplates()
            print("All Templates:")
            print(json.dumps(allTemplates, indent=4))
        except Exception as e:
            print(f"Error retrieving templates: {e}")

    def testGetTemplateByUID(self, templateUID: str):
        """Retrieve a specific template by UID"""
        print("\n~~~~ Test #2 getTemplateByUid(templateUID) ~~~~\n")

        try:
            specificTemplate = self.templatesAPI.getTemplateByUID(templateUID)
            print("Template Details:")
            print(json.dumps(specificTemplate, indent=4))
        except Exception as e:
            print(f"Error retrieving template {templateUID}: {e}")
