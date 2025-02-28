import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Systeminfo

class SysteminfoTest:
    def __init__(self, client: OpenHABClient):
        self.systemInfoAPI = Systeminfo(client)

    def testGetSystemInfo(self):
        """Retrieve system information"""
        print("\n~~~~ Test #1 getSystemInfo() ~~~~\n")

        try:
            systemInfo = self.systemInfoAPI.getSystemInfo()
            print(json.dumps(systemInfo, indent=4))
        except Exception as e:
            print(f"Error retrieving system information: {e}")

    def testGetUoMInfo(self):
        """Retrieve unit of measurement (UoM) information"""
        print("\n~~~~ Test #2 getUomInfo() ~~~~\n")

        try:
            uomInfo = self.systemInfoAPI.getUoMInfo()
            print(json.dumps(uomInfo, indent=4))
        except Exception as e:
            print(f"Error retrieving UoM information: {e}")

