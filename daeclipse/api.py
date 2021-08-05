"""Class to handle making calls to the DeviantArt Eclipse API."""

import json
import re

import browser_cookie3
import requests
from bs4 import BeautifulSoup
from html_to_draftjs import html_to_draftjs

from daeclipse.models.deviationextended import EclipseDeviationExtended
from daeclipse.models.folder import EclipseFolder
from daeclipse.models.groupslist import EclipseGroupsList


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
            EclipseGroupsList: EclipseGroupsList instance.

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
        return EclipseGroupsList(rjson)

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

    def get_deviation_tags(self, deviation_url):
        """Get list of tags for the provided deviation_id.

        Args:
            deviation_url (string): Deviation URL.

        Returns:
            string[]: List of tags.
        """
        queries = {
            'deviationid': get_deviation_id(deviation_url),
            'username': get_username_from_url(deviation_url),
            'type': 'art',
            'include_session': 'false',
        }
        extended_fetch_url = ''.join([
            self.base_uri,
            '/shared_api/deviation/extended_fetch',
            query_string(queries),
        ])
        response = requests.get(extended_fetch_url, cookies=self.cookies)
        rjson = json.loads(response.text)
        deviation_extended = EclipseDeviationExtended(rjson)
        return deviation_extended.deviation.get_tag_names()

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

    def post_status(self, deviation_url, html_content):
        """Create a status to sta.sh and publish from sta.sh to DeviantArt.

        Args:
            deviation_url (string): Deviation URL, just for CSRF purposes.
            html_content (string): Text content of message in HTML-format.

        Returns:
            string: Success message of result.
        """
        # POST /status/create creates a sta.sh post from the provided payload.
        create_status_url = ''.join([
            self.base_uri,
            '/shared_api/status/create',
        ])
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.deviantart.com',
            'referer': deviation_url,
        }
        csrf_token = get_csrf(deviation_url, self.cookies)
        payload = json.dumps({
            'csrf_token': csrf_token,
            'editorRaw': json.dumps(html_to_draftjs(html_content))
        })
        response = requests.post(
            create_status_url,
            cookies=self.cookies,
            headers=headers,
            data=payload,
        )
        rjson = json.loads(response.text)
        if not rjson.get('deviation') or 'error' in rjson:
            print(response.status_code)
            raise_error(rjson)

        # POST /status/publish moves the status from sta.sh to DeviantArt.
        publish_status_url = ''.join([
            self.base_uri,
            '/shared_api/status/publish',
        ])
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
        }
        # statusid is the sta.sh ID, not the production DeviantArt status ID.
        payload = json.dumps({
            'csrf_token': csrf_token,
            'statusid': rjson['deviation'].get('deviationId')
        })
        response = requests.post(
            publish_status_url,
            cookies=self.cookies,
            headers=headers,
            data=payload,
        )
        rjson = json.loads(response.text)
        if not rjson.get('deviation') or 'error' in rjson:
            raise_error(rjson)
        return '✅ Status created: {0}'.format(rjson['deviation'].get('url'))


def get_deviation_id(deviation_url):
    """Extract the deviation_id from the full deviantart image URL.

    Args:
        deviation_url (string): Deviation URL.

    Returns:
        string: Deviation ID.
    """
    url_parts = deviation_url.split('-')
    return url_parts[-1]


def get_username_from_url(deviation_url):
    """Regex parse deviation URL to retrieve username.

    Args:
        deviation_url (string): Deviation URL.

    Raises:
        RuntimeError: If username is not present in URL string.

    Returns:
        string: DeviantArt username.
    """
    username = re.search('deviantart.com/(.+?)/art/', deviation_url)
    if username:
        return username.group(1)
    raise RuntimeError('DeviantArt username not found in URL.')


def get_csrf(deviation_url, cookies):
    """Scrape deviation page for CSRF token.

    Args:
        deviation_url (string): Deviation URL.
        cookies (http.cookiejar.CookieJar): .deviantart.com Cookie Jar.

    Returns:
        string: CSRF validation token.

    Raises:
        RuntimeError: Unable to retrieve CSRF token from provided URL.
    """
    page = requests.get(deviation_url, cookies=cookies)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Check if CSRF is stored in <input type="hidden" name="validate_token" value="CSRF" />.
    token_element = soup.find('input', {'name': 'validate_token'})
    if token_element is not None:
        return token_element.get('value')

    # Check if window.__CSRF_TOKEN__ = 'CSRF'; snippet is present.
    window_csrf_regex = r"window.__CSRF_TOKEN__ = '(.*)';"
    text = soup.find_all(text=re.compile(window_csrf_regex))
    if len(text) > 0:
        csrf_element = re.search(window_csrf_regex, text[0])
        if csrf_element is not None:
            return csrf_element.group(1)

    raise RuntimeError("Unable to retrieve CSRF token from provided URL.")


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
