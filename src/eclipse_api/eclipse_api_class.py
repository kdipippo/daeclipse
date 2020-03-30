#!/usr/bin/env python
"""Class to handle making calls to the New DeviantArt API available for Eclipse."""

import json
import time
import browser_cookie3
import requests
from .eclipse_helpers import get_csrf, sleep_delay


class DeviantArtEclipseAPI:
    """Class to handle making calls to the New DeviantArt API available for Eclipse."""

    base_uri = "https://www.deviantart.com/_napi/shared_api/deviation"

    def __init__(self):
        """Initialze DeviantArtNAPI by fetching Chrome's DeviantArt-related cookies, extracting
        the csrf token, and storing the deviation_id to perform actions on.

        Args:
            deviation_url (string): optional deviation URL, i.e. https://da.com/art/Art-12345.
        """
        self.cookies = browser_cookie3.chrome(domain_name='.deviantart.com')

    def get_cookies(self):
        """Return the logged-in DeviantArt user's cookies.

        Returns:
            http.cookiejar.CookieJar: .deviantart.com Cookie Jar.
        """
        return self.cookies

    def get_groups(self):
        """Prints information about a subset (~10) of groups the user is a member of."""
        groups_url = f"{self.base_uri}/groups"

        start_time = time.time()
        response = requests.get(groups_url, cookies=self.cookies)
        sleep_delay(start_time)

        rjson = json.loads(response.text)
        print(json.dumps(rjson, indent=2))

    def get_group_folders(self, group_id):
        """Returns folder information for the provided group_id ONLY if the cookies stored are
        of a user who is a member of the provided group_id.

        Args:
            group_id (int): ID number for the group on DeviantArt.

        Returns:
            dict: Dictionary response from the API call.
        """
        group_folders_url = f"{self.base_uri}/group_folders?groupid={group_id}&type=gallery"

        start_time = time.time()
        response = requests.get(group_folders_url, cookies=self.cookies)
        sleep_delay(start_time)

        if response.status_code == 200:
            return json.loads(response.text)
        print(f"ERROR!! Status code in get_group_folders was {response.status_code}")
        return dict()

    def add_deviation_to_group(self, group_id, folder_id, deviation_url):
        """Adds the provided deviation to the specified group's folder; prints status and text.

        Args:
            group_id (int): ID number for the group on DeviantArt.
            folder_id (int): ID number for the folder of the group on DeviantArt.
            deviation_url (string): optional deviation URL, i.e. https://da.com/art/Art-12345.
        """
        csrf_token = get_csrf(deviation_url, self.cookies)
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

        start_time = time.time()
        print("requests.post for add_deviation_to_group")
        response = requests.post(group_add_url, cookies=self.cookies, headers=headers, data=data)
        sleep_delay(start_time)

        print(response.status_code)
        rjson = json.loads(response.text)
        print(json.dumps(rjson, indent=2))

def get_deviation_id(deviation_url):
    """Extract the deviation_id from the full deviantart image URL.

    Args:
        deviation_url (string): deviation URL, i.e. https://da.com/art/Art-12345.
    """
    url_parts = deviation_url.split("-")
    return url_parts[-1]
