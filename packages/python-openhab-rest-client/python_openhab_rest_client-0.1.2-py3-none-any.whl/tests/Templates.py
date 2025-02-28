import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import TemplatesTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    templatesTest = TemplatesTest(client)

    # Example template UID
    templateUID = "example_template_uid"

    # Execute test functions
    templatesTest.testGetAllTemplates()       # Test #1
    templatesTest.testGetTemplateByUID(templateUID)  # Test #2
