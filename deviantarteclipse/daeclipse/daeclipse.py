#!/usr/bin/env python
"""Class to handle making calls to the New DeviantArt API available for Eclipse."""

import json
import time
import browser_cookie3
import requests
from bs4 import BeautifulSoup


class dAEclipse:
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

    def get_deviation_tags(self, deviation_id, deviation_username):
        """Get list of tags for the provided deviation_id.

        Args:
            deviation_id (int): ID for the deviation.
            deviation_username (string): Username for the deviation's artist.

        Returns:
            string[]: list of tags.
        """
        extended_fetch_url = f"{self.base_uri}/extended_fetch?deviationid={deviation_id}&username={deviation_username}&type=art&include_session=false"

        # start_time = time.time()
        response = requests.get(extended_fetch_url, cookies=self.cookies)
        # sleep_delay(start_time)

        rjson = json.loads(response.text)
        # tags_objects is a list of objects containing "name" and "url" attributes.
        tags_objects = rjson['deviation']['extended'].get('tags')
        if not tags_objects:
            # "tags" doesn't exist on result payload
            return []
        return [tag['name'] for tag in rjson['deviation']['extended']['tags']]

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

def get_csrf(deviation_url, cookies):
    """Parses the HTML of the deviation to get the csrf token in the page. It's stored as the
    value of a hidden input with name 'validate_token'.

    Args:
        deviation_url (string): deviation URL, i.e. https://da.com/art/Art-12345.
        cookie (http.cookiejar.CookieJar): .deviantart.com Cookie Jar.

    Returns:
        string: CSRF validation token.
    """
    start_time = time.time()
    print("requests.get for get_csrf")
    page = requests.get(deviation_url, cookies=cookies)
    sleep_delay(start_time)

    soup = BeautifulSoup(page.text, 'html.parser')
    return soup.find("input", {"name":"validate_token"})["value"]

def get_group_id(group_name):
    """Parses the HTML of a DeviantArt group page to extract the group's Eclispe ID from two
    possible places on the page.

    Args:
        group_name (string): DeviantArt group name.

    Returns:
        string: Eclipse group ID.
    """
    group_url = f"https://www.deviantart.com/{group_name}"

    start_time = time.time()
    page = requests.get(group_url)
    sleep_delay(start_time)

    soup = BeautifulSoup(page.text, 'html.parser')
    gmi = soup.find("div", {"name":"gmi-GBadge"})
    if gmi is not None:
        return gmi["gmi-owner"]
    gmi = soup.find("div", {"name":"gmi-Gruser"})
    if gmi is not None:
        return gmi["gmi-id"]
    print("ERROR")
    return None


def sleep_without_freeze(delay):
    """Pauses for a provided delay period without causing the script to freeze.

    Args:
        delay (int): Time in seconds to pause.
    """
    start = time.time()
    curr_seconds = int(start)
    curr_time = time.time()
    while curr_time < (start + delay):
        if int(curr_time) > curr_seconds:
            print('.', end='')
            curr_seconds = int(curr_time)
        curr_time = time.time()
    print()


def sleep_delay(start):
    """Pause the program for 15 times the duration of any call made to DeviantArt.

    Args:
        start (float): Unix timestamp representing the start time.
    """
    # wait 10x longer than it took them to respond
    response_delay = int(15 * (time.time() - start))
    print(f"                                 Sleeping {response_delay} seconds")
    sleep_without_freeze(response_delay)
