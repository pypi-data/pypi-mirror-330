import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Logging

class LoggingTest:
    def __init__(self, client: OpenHABClient):
        self.loggingAPI = Logging(client)

    def testGetAllLoggers(self):
        """ Test retrieving all loggers """
        print("\n~~~~ Test #1: getAllLoggers() ~~~~\n")
        try:
            loggers = self.loggingAPI.getAllLoggers()
            print("All loggers:", loggers)
        except Exception as e:
            print(f"Error retrieving loggers: {e}")

    def testGetSingleLogger(self, loggerName: str):
        """ Test retrieving a specific logger """
        print(f"\n~~~~ Test #2: getSingleLogger({loggerName}) ~~~~\n")
        try:
            logger = self.loggingAPI.getSingleLogger(loggerName)
            print(f"Logger {loggerName}:", logger)
        except Exception as e:
            print(f"Error retrieving logger {loggerName}: {e}")

    def testModifyOrAddLogger(self, loggerName: str, level: str):
        """ Test modifying or adding a logger """
        print(f"\n~~~~ Test #3: modifyOrAddLogger({loggerName}, {level}) ~~~~\n")
        try:
            response = self.loggingAPI.modifyOrAddLogger(loggerName, level)
            print(f"Logger {loggerName} modified:", response)
        except Exception as e:
            print(f"Error modifying logger {loggerName}: {e}")

    def testRemoveLogger(self, loggerName: str):
        """ Test removing a logger """
        print(f"\n~~~~ Test #4: removeLogger({loggerName}) ~~~~\n")
        try:
            response = self.loggingAPI.removeLogger(loggerName)
            print(f"Logger {loggerName} removed:", response)
        except Exception as e:
            print(f"Error removing logger {loggerName}: {e}")
