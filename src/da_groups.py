#!/usr/bin/env python
"""This script takes a deviation url and automatically sends submission requests to groups based
on the category the image falls into."""

import json
import requests
import browser_cookie3
from bs4 import BeautifulSoup

class DeviantArtNAPI:
    """Class to handle making calls to the New DeviantArt API available for Eclipse."""

    base_uri = "https://www.deviantart.com/_napi/shared_api/deviation"
    deviation_id = None
    csrf_token = None

    def __init__(self, deviation_url):
        """Initialze DeviantArtNAPI by fetching Chrome's DeviantArt-related cookies, extracting
        the csrf token, and storing the deviation_id to perform actions on.

        Arguments:
            deviation_url {string} -- deviation URL, i.e. https://da.com/art/Artwork-Name-12345.
        """
        self.cookies = browser_cookie3.chrome(domain_name='.deviantart.com')
        self.set_deviation_id(deviation_url)
        self.set_csrf(deviation_url)

    def get_groups(self):
        """Prints information about a subset (~10) of groups the user is a member of."""
        groups_url = f"{self.base_uri}/groups"
        response = requests.get(groups_url, cookies=self.cookies)
        rjson = json.loads(response.text)
        print(json.dumps(rjson, indent=2))

    def get_group_folders(self, group_id):
        """Prints folder information for the provided group_id.

        Arguments:
            group_id {int} -- ID number for the group on DeviantArt.
        """
        group_folders_url = f"{self.base_uri}/group_folders?groupid={group_id}&type=gallery"
        response = requests.get(group_folders_url, cookies=self.cookies)
        rjson = json.loads(response.text)
        print(json.dumps(rjson, indent=2))

    def add_deviation_to_group(self, group_id, folder_id):
        """Adds the provided deviation to the specified group's folder; prints status and text.

        Arguments:
            group_id {int} -- ID number for the group on DeviantArt.
            folder_id {int} -- ID number for the folder of the group on DeviantArt.
        """
        group_add_url = f"{self.base_uri}/group_add"
        headers = {
            "accept": 'application/json, text/plain, */*',
            "content-type": 'application/json;charset=UTF-8'
        }
        data = json.dumps({
            "groupid": group_id,
            "type": "gallery",
            "folderid": folder_id,
            "deviationid": self.deviation_id,
            "csrf_token": self.csrf_token
        })
        response = requests.post(group_add_url, cookies=self.cookies, headers=headers, data=data)
        print(response.status_code)
        rjson = json.loads(response.text)
        print(json.dumps(rjson, indent=2))

    def set_csrf(self, deviation_url):
        """Parse the HTML of the deviation to get the csrf token in the page. It's stored as the
        value of a hidden input with name 'validate_token'.

        Arguments:
            deviation_url {string} -- deviation URL, i.e. https://da.com/art/Artwork-Name-12345.
        """
        page = requests.get(deviation_url, cookies=self.cookies)
        soup = BeautifulSoup(page.text, 'html.parser')
        self.csrf_token = soup.find("input", {"name":"validate_token"})["value"]

    def set_deviation_id(self, deviation_url):
        """Extract the deviation_id from the full deviantart image URL.

        Arguments:
            deviation_url {string} -- deviation URL, i.e. https://da.com/art/Artwork-Name-12345.
        """
        url_parts = deviation_url.split("-")
        self.deviation_id = url_parts[-1]

if __name__ == "__main__":
    # working, only gives 10 - deviantart.get_groups()
    # working - deviantart.get_group_folders(14718292)
    # not working - deviantart.add_deviation_to_group(14718292, 63180668, 765976537)
    DEVIATION_URL = "https://www.deviantart.com/pepper-wood/" + \
        "art/Digital-Inktober-Test-2018-765976537"
    CHECK = input("Press enter to confirm that the deviation in Eclipse is open in Chrome: ")
    DEVIANTART = DeviantArtNAPI(DEVIATION_URL)
    DEVIANTART.add_deviation_to_group(
        40852213, # Candycorn-Kingdom
        60854872  # Featured
    )
