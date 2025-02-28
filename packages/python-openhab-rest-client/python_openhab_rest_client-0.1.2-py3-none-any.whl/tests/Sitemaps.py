import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import SitemapsTest

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    sitemapsTest = SitemapsTest(client)

    # Example sitemap name and subscription ID
    sitemapName = "Sitemap"
    subscriptionId = "013328fd-d3fd-4de4-8f7d-efe01bad7eac"

    # Execute test functions
    sitemapsTest.testGetAllSitemaps()                                     # Test #1
    sitemapsTest.testGetSitemap(sitemapName)                            # Test #2
    sitemapsTest.testGetSitemapPage("astro", "astro")                   # Test #3
    sitemapsTest.testGetFullSitemap("astro")                            # Test #4
    sitemapsTest.testGetSitemapEvents(subscriptionId, sitemapName)      # Test #5
    sitemapsTest.testGetFullSitemapEvents(subscriptionId, sitemapName)  # Test #6
