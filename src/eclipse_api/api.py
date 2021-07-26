#!/usr/bin/env python
"""Class to handle making calls to the New DeviantArt API available for Eclipse."""

import json
import time
import browser_cookie3
import requests

from .models import EclipseFolder

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

    def get_groups(self, username, offset, limit = 24):
        """Prints information about a subset (~10) of groups the user is a member of."""
        # limit at most has to be 24.
        # groups_url = f"{self.base_uri}/groups"
        moduleid = "1761969747" # Static value that DeviantArt uses to tie this to the "Get Members" block.
        groups_url = f"https://www.deviantart.com/_napi/da-user-profile/api/module/groups/members?username={username}&moduleid={moduleid}&offset={offset}&limit={limit}"

        response = requests.get(groups_url, cookies=self.cookies)

        rjson = json.loads(response.text)
        return rjson

    def get_group_folders(self, group_id, deviation_url):
        """Returns folder information for the provided group_id ONLY if the cookies stored are
        of a user who is a member of the provided group_id.

        Args:
            group_id (int): ID number for the group on DeviantArt.

        Returns:
            EclipseFolder[]: A list of Eclipse Folder objects.
        """
        group_folders_url = f"{self.base_uri}/group_folders?groupid={group_id}&type=gallery"
        response = requests.get(group_folders_url, cookies=self.cookies, headers={'referer': deviation_url})

        # {'error': 'unauthorized', 'errorDescription': 'Not authorized', 'status': 'error'}
        if 'error' in folder_data:
            return []
        folder_data = json.loads(response.text)
        folders = [EclipseFolder(d) for d in folder_data['results']]
        return folders

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

        response = requests.post(group_add_url, cookies=self.cookies, headers=headers, data=data)

        # {'success': True, 'needsVote': True, 'deviationGroupCount': 1}
        # {'error': 'invalid_request', 'errorDescription': 'Validation failed', 'errorDetails': 'The target folder is over its size limit.', 'status': 'error'}
        rjson = json.loads(response.text)
        if "success" in rjson:
            if rjson["success"] == True:
                if rjson["needsVote"]:
                    return True, "Deviation added to folder and automatically approved"
                else:
                    return True, "Deviation submitted to folder and pending moderator approval"
        if "error" in rjson:
            return False, rjson["errorDetails"]
        print(rjson)
        return True, "idk what happened"

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
    page = requests.get(deviation_url, cookies=cookies)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup.find("input", {"name":"validate_token"})["value"]
