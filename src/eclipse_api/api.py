"""Class to handle making calls to the DeviantArt Eclipse API."""

import json

import browser_cookie3
import requests
from bs4 import BeautifulSoup
from models import EclipseFolder


class DeviantArtEclipseAPI:
    """Class to handle making calls to the DeviantArt Eclipse API."""

    base_uri = "https://www.deviantart.com/_napi"

    def __init__(self):
        """Initialize API by fetching Chrome's DeviantArt-related cookies."""
        self.cookies = browser_cookie3.chrome(domain_name='.deviantart.com')

    def get_cookies(self):
        """Return the logged-in DeviantArt user's cookies.

        Returns:
            http.cookiejar.CookieJar: .deviantart.com Cookie Jar.
        """
        return self.cookies

    def get_groups(self, username, offset, limit=24):
        """Return a subset of the user's joined DeviantArt groups.

        Args:
            username (string): DeviantArt username of user.
            offset (int): Offset to start with API call.
            limit (int, optional): Limit of results to return. Defaults to 24.

        Returns:
            dict: Raw API response from API call.

        Raises:
            ValueError: If `limit` is greater than 24.
        """
        if limit > 24:
            raise ValueError('Limit must be equal to or below 24.')

        queries = {
            'username': username,
            'moduleid': '1761969747',  # "Get Members" block ID.
            'offset': offset,
            'limit': limit,
        }
        groups_url = ''.join([
            self.base_uri,
            '/da-user-profile/api/module/groups/members',
            query_string(queries),
        ])

        response = requests.get(groups_url, cookies=self.cookies)

        rjson = json.loads(response.text)
        return rjson

    def get_group_folders(self, group_id, deviation_url):
        """Returns folder information for the provided group_id ONLY, if
         cookies belong to a member of the group.

        Args:
            group_id (int): Group ID.

        Returns:
            EclipseFolder[]: List of EclipseFolder objects.

        Raises:
            RuntimeError: If API call returns an error payload.
        """
        group_folders_url = ''.join([
            self.base_uri,
            '/shared_api/deviation/group_folders',
            query_string({'groupid': group_id, 'type': 'gallery'}),
        ])
        headers = {'referer': deviation_url}
        response = requests.get(
            group_folders_url,
            cookies=self.cookies,
            headers=headers,
        )

        folder_data = json.loads(response.text)
        if 'error' in folder_data:
            raise RuntimeError(folder_data['errorDetails'])
        folders = [EclipseFolder(d) for d in folder_data['results']]
        return folders

    def add_deviation_to_group(self, group_id, folder_id, deviation_url):
        """Submit deviation to the specified folder in group.

        Args:
            group_id (int): Group ID.
            folder_id (int): Folder ID.
            deviation_url (string): Deviation URL.

        Returns:
            string: Success message of result.

        Raises:
            RuntimeError: If API call returns an error payload.
        """
        csrf_token = get_csrf(deviation_url, self.cookies)
        deviation_id = get_deviation_id(deviation_url)

        group_add_url = ''.join([
            self.base_uri,
            '/shared_api/deviation/group_add',
        ])
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8'
        }
        data = json.dumps({
            'groupid': group_id,
            'type': 'gallery',
            'folderid': folder_id,
            'deviationid': deviation_id,
            'csrf_token': csrf_token,
        })

        response = requests.post(
            group_add_url,
            cookies=self.cookies,
            headers=headers,
            data=data,
        )

        rjson = json.loads(response.text)
        if 'error' in rjson:
            raise RuntimeError(rjson['errorDetails'])
        if rjson['needsVote']:
            return 'Deviation added to folder and automatically approved'
        return 'Deviation submitted to folder and pending moderator approval'

def get_deviation_id(deviation_url):
    """Extract the deviation_id from the full deviantart image URL.

    Args:
        deviation_url (string): Deviation URL.
    """
    url_parts = deviation_url.split('-')
    return url_parts[-1]

def get_csrf(deviation_url, cookies):
    """Scrape deviation page to retrieve CSRF token stored as hidden input with
    name 'validate_token'.

    Args:
        deviation_url (string): Deviation URL.
        cookie (http.cookiejar.CookieJar): .deviantart.com Cookie Jar.

    Returns:
        string: CSRF validation token.
    """
    page = requests.get(deviation_url, cookies=cookies)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup.find('input', {'name':'validate_token'})['value']

def query_string(query_dict):
    """Convert a dictionary into a query string URI.

    Args:
        query_dict (dict): Dictionary of query keys and values.

    Returns:
        string: Query string, i.e. ?query1=value&query2=value.
    """
    queries = [f"{key}={query_dict[key]}" for key in query_dict.keys()]
    queries_string = "&".join(queries)
    return "?" + queries_string
