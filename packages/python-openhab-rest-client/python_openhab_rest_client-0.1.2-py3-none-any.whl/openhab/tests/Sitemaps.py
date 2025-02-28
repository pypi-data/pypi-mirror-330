import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Sitemaps

class SitemapsTest:
    def __init__(self, client: OpenHABClient):
        self.sitemapsAPI = Sitemaps(client)

    def testGetAllSitemaps(self):
        """Retrieve all sitemaps"""
        print("\n~~~~ Test #1 getSitemaps() ~~~~\n")

        try:
            sitemaps = self.sitemapsAPI.getSitemaps()
            print(json.dumps(sitemaps, indent=4))
        except Exception as e:
            print(f"Error retrieving all sitemaps: {e}")

    def testGetSitemap(self, sitemapName: str):
        """Retrieve a specific sitemap"""
        print("\n~~~~ Test #2 getSitemap(sitemapName) ~~~~\n")

        try:
            sitemap = self.sitemapsAPI.getSitemap(sitemapName)
            print(json.dumps(sitemap, indent=4))
        except Exception as e:
            print(f"Error retrieving sitemap {sitemapName}: {e}")

    def testGetSitemapPage(self, sitemapName: str, pageID: str):
        """Retrieve a specific sitemap page"""
        print("\n~~~~ Test #3 getSitemapPage(sitemapName, pageID) ~~~~\n")

        try:
            sitemapPage = self.sitemapsAPI.getSitemapPage(sitemapName, pageID)
            print(json.dumps(sitemapPage, indent=4))
        except Exception as e:
            print(f"Error retrieving sitemap page {pageID} from {sitemapName}: {e}")

    def testGetFullSitemap(self, sitemapName: str):
        """Retrieve all data of a sitemap"""
        print("\n~~~~ Test #4 getFullSitemap(sitemapName) ~~~~\n")

        try:
            fullSitemap = self.sitemapsAPI.getFullSitemap(sitemapName)
            print(json.dumps(fullSitemap, indent=4))
        except Exception as e:
            print(f"Error retrieving full sitemap {sitemapName}: {e}")

    def testGetSitemapEvents(self, subscriptionId: str, sitemapName: str):
        """Retrieve events for a sitemap"""
        print("\n~~~~ Test #5 getSitemapEvents(subscriptionId, sitemapName) ~~~~\n")

        try:
            sitemapEvents = self.sitemapsAPI.getSitemapEvents(subscriptionId, sitemap=sitemapName)
            print(json.dumps(sitemapEvents, indent=4))
        except Exception as e:
            print(f"Error retrieving events for sitemap {sitemapName}: {e}")

    def testGetFullSitemapEvents(self, subscriptionId: str, sitemapName: str):
        """Retrieve events for the entire sitemap"""
        print("\n~~~~ Test #6 getFullSitemapEvents(subscriptionId, sitemapName) ~~~~\n")

        try:
            fullSitemapEvents = self.sitemapsAPI.getFullSitemapEvents(subscriptionId, sitemap=sitemapName)
            print(json.dumps(fullSitemapEvents, indent=4))
        except Exception as e:
            print(f"Error retrieving full sitemap events for {sitemapName}: {e}")
