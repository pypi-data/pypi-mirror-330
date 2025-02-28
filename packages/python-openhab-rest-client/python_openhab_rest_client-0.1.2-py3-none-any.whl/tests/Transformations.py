import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import TransformationsTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    transformationsTest = TransformationsTest(client)

    # Example transformation transformationUID and updated data
    transformationUID = "en.map"
    updatedData = {
        "uid": "my_custom_map",
        "label": "My Custom Map",
        "type": "map",
        "configuration": {"function": "CLOSED=closed\nOPEN=open\nNULL=unknown\n"},
        "editable": True
    }

    # Execute test functions
    transformationsTest.testGetTransformations()                                      # Test #1
    transformationsTest.testGetTransformation(transformationUID)                    # Test #2
    transformationsTest.testUpdateTransformation(transformationUID, updatedData)    # Test #3
    transformationsTest.testDeleteTransformation(transformationUID)                 # Test #4
    transformationsTest.testGetTransformationServices()                               # Test #5
