import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Transformations

class TransformationsTest:
    def __init__(self, client: OpenHABClient):
        self.discoveryAPI = Transformations(client)

    def testGetTransformations(self):
        """Retrieve all transformations"""
        print("\n~~~~ Test #1: getTransformations() ~~~~\n")

        try:
            transformations = self.transformationsAPI.getTransformations()
            print(json.dumps(transformations, indent=4))
        except Exception as e:
            print(f"Error retrieving transformations: {e}")

    def testGetTransformation(self, transformationUID: str):
        """Retrieve a specific transformation by transformationUID"""
        print("\n~~~~ Test #2: getTransformation(transformationUID) ~~~~\n")

        try:
            transformation = self.transformationsAPI.getTransformation(transformationUID)
            print(json.dumps(transformation, indent=4))
        except Exception as e:
            print(f"Error retrieving transformation {transformationUID}: {e}")

    def testUpdateTransformation(self, transformationUID: str, updatedData: dict):
        """Update a specific transformation by transformationUID"""
        print("\n~~~~ Test #3: updateTransformation(transformationUID, updatedData) ~~~~\n")

        try:
            response = self.transformationsAPI.updateTransformation(transformationUID, updatedData)
            print(f"Updated transformation {transformationUID}:\n{json.dumps(response, indent=4)}")
        except Exception as e:
            print(f"Error updating transformation {transformationUID}: {e}")

    def testDeleteTransformation(self, transformationUID: str):
        """Delete a specific transformation by transformationUID"""
        print("\n~~~~ Test #4: deleteTransformation(transformationUID) ~~~~\n")

        try:
            self.transformationsAPI.deleteTransformation(transformationUID)
            print(f"Transformation {transformationUID} deleted successfully.")
        except Exception as e:
            print(f"Error deleting transformation {transformationUID}: {e}")

    def testGetTransformationServices(self):
        """Retrieve all available transformation services"""
        print("\n~~~~ Test #5: getTransformationServices() ~~~~\n")

        try:
            services = self.transformationsAPI.getTransformationServices()
            print(json.dumps(services, indent=4))
        except Exception as e:
            print(f"Error retrieving transformation services: {e}")
