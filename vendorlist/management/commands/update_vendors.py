from django.core.management.base import BaseCommand, CommandError
from vendorlist.models import Vendor

import requests
from lxml import html


class Command(BaseCommand):
    """Scrapes the offthegridsf website for vendor information and updates the database."""

    vendor_site = "http://offthegridsf.com/vendors"
    help = "Scrapes %s for new vendors." % vendor_site

    def handle(self, *args, **options):
        """Download the vendor list site and update the Vendor table."""

        print "Scraping the offthegridsf website..."
        
        if args:
            testing_mode = args[0]=="test" #If tests are being run, args[0] is always 'test'
        else:
            testing_mode = False

        vendor_data_elements = self.get_vendor_data_elements(testing_mode)

        print "Updating database..."
        for vendor_data in vendor_data_elements:
            self.add_vendor_to_db(vendor_data)
        
        print "Success!"

    def get_vendor_data_elements(self, testing_mode):
        """Get all the vendor elements from the page and return a list."""
        html_string = self.get_website(self.vendor_site, testing_mode)
        root = html.fromstring(html_string)
        return root.find_class("otg-vendor-data")

    def get_website(self, site, is_testing=False):
        """Returns the html string for a site."""

        if is_testing:
            print "Loading data from disk..."
            with open("vendorlist/test_data/vendor_site.html") as f:
                return f.read()

        try:
            request = requests.get(site)
        except requests.exceptions.ConnectionError:
            raise CommandError("Couldn't connect to %s." % site)

        return request.content

    def add_vendor_to_db(self, vendor_data):
        """Creates a Vendor and adds it to the database."""
        name, website = self.get_name_website_pair(vendor_data)

        vendor, created = Vendor.objects.update_or_create_vendor(name=name, website=website)

    def get_name_website_pair(self, vendor_data):
        try:
            vendor_name_link = vendor_data.find_class("otg-vendor-name-link")[0]
        except IndexError:
            return

        name = vendor_name_link.text_content().strip()
        website = vendor_name_link.attrib["href"]

        return name, website
