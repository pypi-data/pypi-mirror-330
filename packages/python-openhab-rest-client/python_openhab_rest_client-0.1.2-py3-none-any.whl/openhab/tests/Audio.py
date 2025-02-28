import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Audio

class AudioTest:
    def __init__(self, client: OpenHABClient):
        self.audioAPI = Audio(client)

    # Test the endpoint to get the default sink
    def testGetDefaultSink(self, language: str = None):
        print("\n~~~~ Test #1 getDefaultSink() ~~~~\n")

        try:
            response = self.audioAPI.getDefaultSink(language)
            print(response)
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test the endpoint to get the default source
    def testGetDefaultSource(self, language: str = None):
        print("\n~~~~ Test #2 getDefaultSource() ~~~~\n")

        try:
            response = self.audioAPI.getDefaultSource(language)
            print(response)
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test the endpoint to get all sinks
    def testGetSinks(self, language: str = None):
        print("\n~~~~ Test #3 getSinks() ~~~~\n")

        try:
            response = self.audioAPI.getSinks(language)
            print(response)
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test the endpoint to get all sources
    def testGetSources(self, language: str = None):
        print("\n~~~~ Test #4 getSources() ~~~~\n")

        try:
            response = self.audioAPI.getSources(language)
            print(response)
        except Exception as e:
            print(f"Error executing action: {e}")
