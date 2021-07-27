"""Class to handle making calls to the DeviantArt Eclipse API."""

import json

import browser_cookie3
import requests
from bs4 import BeautifulSoup

from daeclipse.models.folder import EclipseFolder
from daeclipse.models.gruser import EclipseGruser


class Eclipse(object):
    """Class to handle making calls to the DeviantArt Eclipse API."""

    base_uri = 'https://www.deviantart.com/_napi'

    def __init__(self):
        """Initialize API by fetching Chrome's DeviantArt-related cookies."""
        self.cookies = browser_cookie3.chrome(domain_name='.deviantart.com')

    def get_groups(self, username, offset, limit=24):
        """Return a paginated call for the user's joined DeviantArt groups.

        Args:
            username (string): DeviantArt username of user.
            offset (int): Offset to start with API call.
            limit (int, optional): Limit of results to return. Defaults to 24.

        Returns:
            EclipseGruser[]: List of Eclipse group objects.
            bool: If there are more results.
            int: Next offset to query for more paginated results.
            int: Total number of groups user is a member of.

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
        groups = [EclipseGruser(group) for group in rjson['results']]
        return groups, rjson['hasMore'], rjson['nextOffset'], rjson['total']

    def get_group_folders(self, group_id, deviation_url):
        """Return folders for group, if user is member of group.

        Args:
            group_id (int): Group ID.
            deviation_url (string): Deviation URL.

        Returns:
            EclipseFolder[]: List of EclipseFolder objects.
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
            raise_error(folder_data)
        return [EclipseFolder(folder) for folder in folder_data['results']]

    def add_deviation_to_group(self, group_id, folder_id, deviation_url):
        """Submit deviation to the specified folder in group.

        Args:
            group_id (int): Group ID.
            folder_id (int): Folder ID.
            deviation_url (string): Deviation URL.

        Returns:
            string: Success message of result.
        """
        group_add_url = ''.join([
            self.base_uri,
            '/shared_api/deviation/group_add',
        ])
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
        }
        payload = json.dumps({
            'groupid': group_id,
            'type': 'gallery',
            'folderid': folder_id,
            'deviationid': get_deviation_id(deviation_url),
            'csrf_token': get_csrf(deviation_url, self.cookies),
        })

        response = requests.post(
            group_add_url,
            cookies=self.cookies,
            headers=headers,
            data=payload,
        )

        rjson = json.loads(response.text)
        if 'error' in rjson:
            raise_error(rjson)
        if rjson['needsVote']:
            return '✅ Deviation added to folder and automatically approved'
        return '⌛ Deviation submitted to folder and pending mod approval'


def get_deviation_id(deviation_url):
    """Extract the deviation_id from the full deviantart image URL.

    Args:
        deviation_url (string): Deviation URL.

    Returns:
        string: Deviation ID.
    """
    url_parts = deviation_url.split('-')
    return url_parts[-1]


def get_csrf(deviation_url, cookies):
    """Scrape deviation page for CSRF token.

    Args:
        deviation_url (string): Deviation URL.
        cookies (http.cookiejar.CookieJar): .deviantart.com Cookie Jar.

    Returns:
        string: CSRF validation token.
    """
    page = requests.get(deviation_url, cookies=cookies)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup.find('input', {'name': 'validate_token'})['value']


def query_string(query_dict):
    """Convert a dictionary into a query string URI.

    Args:
        query_dict (dict): Dictionary of query keys and values.

    Returns:
        string: Query string, i.e. ?query1=value&query2=value.
    """
    queries = [
        '{0}={1}'.format(key, query_dict[key]) for key in query_dict.keys()
    ]
    queries_string = '&'.join(queries)
    return '?{0}'.format(queries_string)


def raise_error(error_response):
    """Throw RuntimeError with appropriate error message.

    Args:
        error_response (dict): Raw API error response.

    Raises:
        RuntimeError: Error with message from error_response payload.
    """
    if 'errorDetails' in error_response:
        raise RuntimeError(error_response.get('errorDetails'))
    if 'errorDescription' in error_response:
        raise RuntimeError(error_response.get('errorDescription'))
    raise RuntimeError(str(error_response))
