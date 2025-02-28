import sys
import os
from datetime import datetime
import pytz

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient
from openhab.tests import ActionsTest

if __name__ == "__main__":
    # Initialize OpenHAB client (replace with your OpenHAB URL and authentication details)
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    actionsTest = ActionsTest(client)

    # Retrieve all available actions for a given Thing
    thingUID = "astro:sun:b54938fe5c"  # Example Thing UID

    # Define an action to execute
    actionUID = "astro.getEventTime"  # Example action UID

    # Prepare input data (choosing phase "SUNSET" as an example)
    phaseName = "SUN_SET"  # Correctly written phase name (e.g., "SUNRISE", "SUNSET", "NOON")
    momentValue = "START"  # Default value for "moment" is "START"

    # Get current date and time in ISO 8601 format with timezone (ZonedDateTime)
    now = datetime.now(pytz.utc)
    dateValueZoned = now.strftime('%Y-%m-%dT%H:%M:%S%z')  # Format: "2025-01-27T14:30:00+00:00"

    # Prepare input parameters for the action
    actionInputs = {
        "phaseName": phaseName,  # Required phase name
        "date": str(dateValueZoned),  # Date in correct ZonedDateTime format
        "moment": momentValue  # Moment (START or END)
    }

    # Execute all tests
    actionsTest.testGetAllActions(thingUID)                             # Test #1
    actionsTest.testExecuteAction(thingUID, actionUID, actionInputs)    # Test #2