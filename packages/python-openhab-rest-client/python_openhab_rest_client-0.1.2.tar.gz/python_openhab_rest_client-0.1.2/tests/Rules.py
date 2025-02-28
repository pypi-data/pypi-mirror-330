import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import RulesTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    rulesTest = RulesTest(client)

    # Example rule data
    ruleID = "test_color-1"
    newRuleData = {
        "uid": "newRule",
        "name": "New Rule",
        "description": "This is a new rule",
        "triggers": [],
        "conditions": [],
        "actions": []
    }
    updateData = {"name": "Updated Rule"}

    # Execute functions
    rulesTest.testGetAllRules()                       # Test #1
    rulesTest.testGetRuleDetails(ruleID)            # Test #2
    rulesTest.testCreateRule(newRuleData)           # Test #3
    rulesTest.testUpdateRule("newRule", updateData) # Test #4
    rulesTest.testSetRuleState("newRule", True)     # Test #5
    rulesTest.testSetRuleState("newRule", False)    # Test #5
    rulesTest.testExecuteRuleNow(ruleID)            # Test #6
    rulesTest.testDeleteRule("newRule")             # Test #7
