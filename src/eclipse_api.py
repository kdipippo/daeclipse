#!/usr/bin/env python
"""Class to handle making calls through the DeviantArt Eclipse API."""

import browser_cookie3
import json
import requests
from bs4 import BeautifulSoup

class DeviantArtEclipseAPI:
    """Class to handle making calls to the New DeviantArt API available for Eclipse."""

    base_uri = "https://www.deviantart.com/_napi/shared_api/deviation"

    def __init__(self):
        """Initialze DeviantArtNAPI by fetching Chrome's DeviantArt-related cookies, extracting
        the csrf token, and storing the deviation_id to perform actions on.

        Arguments:
            deviation_url {string} -- optional deviation URL, i.e. https://da.com/art/Art-12345.
        """
        self.cookies = browser_cookie3.chrome(domain_name='.deviantart.com')

    def get_cookies(self):
        """Return the ???

        Returns:
            [type] -- [description]
        """
        print(self.cookies)
        return self.cookies

    def get_csrf(self, deviation_url):
        """Parses the HTML of the deviation to get the csrf token in the page. It's stored as the
        value of a hidden input with name 'validate_token'.

        Arguments:
            deviation_url {string} -- deviation URL, i.e. https://da.com/art/Art-12345.
        """
        page = requests.get(deviation_url, cookies=self.cookies)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup.find("input", {"name":"validate_token"})["value"]

    def get_groups(self):
        """Prints information about a subset (~10) of groups the user is a member of."""
        groups_url = f"{self.base_uri}/groups"
        response = requests.get(groups_url, cookies=self.cookies)
        rjson = json.loads(response.text)
        print(json.dumps(rjson, indent=2))

    def get_group_id(self, group_name):
        group_url = f"https://www.deviantart.com/{group_name}"
        page = requests.get(group_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        gmi = soup.find("div", {"name":"gmi-GBadge"})
        if gmi is not None:
            return gmi["gmi-owner"]
        gmi = soup.find("div", {"name":"gmi-Gruser"})
        if gmi is not None:
            return gmi["gmi-id"]
        print("ERROR")
        return None



    def get_group_folders(self, group_id):
        """Returns folder information for the provided group_id ONLY if the cookies stored are
        of a user who is a member of the provided group_id.

        Arguments:
            group_id {int} -- ID number for the group on DeviantArt.

        Returns:
            dict -- Dictionary response from the API call.
        """
        group_folders_url = f"{self.base_uri}/group_folders?groupid={group_id}&type=gallery"
        response = requests.get(group_folders_url, cookies=self.cookies)
        if response.status_code == 200:
            return json.loads(response.text)
        print(f"ERROR!! Status code in get_group_folders was {response.status_code}")
        return dict()

    def add_deviation_to_group(self, group_id, folder_id, deviation_url):
        """Adds the provided deviation to the specified group's folder; prints status and text.

        Arguments:
            group_id {int} -- ID number for the group on DeviantArt.
            folder_id {int} -- ID number for the folder of the group on DeviantArt.
            deviation_url {string} -- optional deviation URL, i.e. https://da.com/art/Art-12345.
        """
        csrf_token = self.get_csrf(deviation_url)
        deviation_id = get_deviation_id(deviation_url)

        group_add_url = f"{self.base_uri}/group_add"
        headers = {
            "accept": 'application/json, text/plain, */*',
            "content-type": 'application/json;charset=UTF-8'
        }
        data = json.dumps({
            "groupid": group_id,
            "type": "gallery",
            "folderid": folder_id,
            "deviationid": deviation_id,
            "csrf_token": csrf_token
        })
        response = requests.post(group_add_url, cookies=self.cookies, headers=headers, data=data)
        print(response.status_code)
        rjson = json.loads(response.text)
        print(json.dumps(rjson, indent=2))

def get_deviation_id(deviation_url):
    """Extract the deviation_id from the full deviantart image URL.

    Arguments:
        deviation_url {string} -- deviation URL, i.e. https://da.com/art/Art-12345.
    """
    url_parts = deviation_url.split("-")
    return url_parts[-1]