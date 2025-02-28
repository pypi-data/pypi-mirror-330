import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Iconsets

class IconsetsTest:
    def __init__(self, client: OpenHABClient):
        self.iconsetsAPI = Iconsets(client)

    # Test retrieving all Iconsets
    def testGetAllIconsets(self, language: str = None):
        print("\n~~~~ Test #1: getAllIconsets() ~~~~\n")

        try:
            iconsets = self.iconsetsAPI.getAllIconsets(language)
            print("Available Iconsets:", iconsets)
        except Exception as e:
            print("Error retrieving Iconsets:", e)
