import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import LoggingTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    loggingTest = LoggingTest(client)

    # Test variables
    loggerName = "org.openhab"
    loggerLevel = "DEBUG"

    # Run tests
    loggingTest.testGetAllLoggers()                             # Test #1
    loggingTest.testGetSingleLogger(loggerName)                 # Test #2
    loggingTest.testModifyOrAddLogger(loggerName, loggerLevel)  # Test #3
    loggingTest.testRemoveLogger(loggerName)                    # Test #4
