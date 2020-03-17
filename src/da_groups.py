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

    def get_groups(self):
        """Prints information about a subset (~10) of groups the user is a member of."""
        groups_url = f"{self.base_uri}/groups"
        response = requests.get(groups_url, cookies=self.cookies)
        rjson = json.loads(response.text)
        print(json.dumps(rjson, indent=2))

    def get_group_folders(self, group_id):
        """Returns folder information for the provided group_id.

        Arguments:
            group_id {int} -- ID number for the group on DeviantArt.

        Returns:
            string -- Full text response from the API call.
        """
        group_folders_url = f"{self.base_uri}/group_folders?groupid={group_id}&type=gallery"
        response = requests.get(group_folders_url, cookies=self.cookies)
        return response.text

    def add_deviation_to_group(self, group_id, folder_id, deviation_url):
        """Adds the provided deviation to the specified group's folder; prints status and text.

        Arguments:
            group_id {int} -- ID number for the group on DeviantArt.
            folder_id {int} -- ID number for the folder of the group on DeviantArt.
            deviation_url {string} -- optional deviation URL, i.e. https://da.com/art/Art-12345.
        """
        csrf_token = get_csrf(deviation_url, self.get_cookies())
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

def get_csrf(deviation_url, cookies):
    """Parse the HTML of the deviation to get the csrf token in the page. It's stored as the
    value of a hidden input with name 'validate_token'.

    Arguments:
        deviation_url {string} -- deviation URL, i.e. https://da.com/art/Art-12345.
    """
    page = requests.get(deviation_url, cookies=cookies)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup.find("input", {"name":"validate_token"})["value"]

def get_deviation_id(deviation_url):
    """Extract the deviation_id from the full deviantart image URL.

    Arguments:
        deviation_url {string} -- deviation URL, i.e. https://da.com/art/Art-12345.
    """
    url_parts = deviation_url.split("-")
    return url_parts[-1]

def getGroupRow(name, id):
    row = f"'name': '{name}', 'id': {id}"
    return row

def getRow(name, id):
    row = f"'name': '{name}', 'id': {id}, 'categories': []"
    return "  { " + row + " },"

def getGroupId(group_name):
    group_url = f"https://www.deviantart.com/{group_name}"
    page = requests.get(group_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup.find("div", {"name":"gmi-Gruser"})["gmi-id"]

if __name__ == "__main__":
    # print("1) Provide a deviation URL and add to groups based on category")
    # print("2) Provide a group name and fetch all the information needed to update da_groups.json")
    # choice = input("Type your option: ")
    choice = "2"
    if choice == "1":
        # example: https://www.deviantart.com/pepper-wood/art/Digital-Inktober-Test-2018-765976537
        print("Please ensure that the deviation is open in Eclipse in Chrome before continuing.")
        DEVIATION_URL = input("Paste deviation URL: ")
        DEVIANTART = DeviantArtNAPI()
        DEVIANTART.add_deviation_to_group(
            40852213, # Candycorn-Kingdom
            60854872, # Featured
            "https://www.deviantart.com/pepper-wood/art/Digital-Inktober-Test-2018-765976537"
        )
    elif choice == "2":
        group_name = input("Please provide the group name: ")
        group_id = getGroupId(group_name)
        print(getGroupRow(group_name, group_id))
        DEVIANTART = DeviantArtNAPI()
        # 4928626; 40852213
        texty = DEVIANTART.get_group_folders(13075062)
        daGroups = json.loads(texty)
        # print(json.dumps(daGroups, indent=2))
        print('"folders": [')
        for folder in daGroups['results']:
            print(getRow(folder['name'], folder['folderId']))
        print(']')
        # THIS IS NOW RETURNING BLANK RESULTS???
        '''
        {
            "results": []
        }
        '''
        # groups I want to fetch: pixelized--world, kawaii-explosion

