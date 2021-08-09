"""Class to handle making calls to the DeviantArt Eclipse API."""

import http
import json
import re

import browser_cookie3
import requests
from bs4 import BeautifulSoup
from html_to_draftjs import html_to_draftjs

from daeclipse.models.deviationextendedresult import DeviationExtendedResult
from daeclipse.models.folder import Folder
from daeclipse.models.groupslist import GroupsList
from daeclipse.models.userscommentslist import UsersCommentsList


class Eclipse(object):
    """Class to handle making calls to the DeviantArt Eclipse API."""

    base_uri = 'https://www.deviantart.com/_napi'

    def __init__(self):
        """Initialize API by fetching Chrome's DeviantArt-related cookies."""
        self.cookies = browser_cookie3.chrome(domain_name='.deviantart.com')

    def get_groups(self, username, offset, limit=24):
        """Return a paginated call for the user's joined DeviantArt groups.

        Args:
            username (str): DeviantArt username of user.
            offset (int): Offset to start with API call.
            limit (int, optional): Limit of results to return. Defaults to 24.

        Returns:
            GroupsList: GroupsList instance.

        Raises:
            ValueError: If `limit` is greater than 24.
        """
        if limit > 24:
            raise ValueError('Limit must be equal to or below 24.')

        queries = {
            'username': username,
            'moduleid': self.get_module_id(username, 'group_list_members'),
            'offset': offset,
            'limit': limit,
        }
        response = requests.get(
            ''.join([
                self.base_uri,
                '/da-user-profile/api/module/groups/members',
                query_string(queries),
            ]),
            cookies=self.cookies,
        )
        rjson = validate_response_succeeds(response)
        return GroupsList(rjson)

    def get_group_folders(self, group_id, deviation_url):
        """Return folders for group, if user is member of group.

        Args:
            group_id (int): Group ID.
            deviation_url (str): Deviation URL.

        Returns:
            Folder[]: List of Folder objects.
        """
        headers = {'referer': deviation_url}
        response = requests.get(
            ''.join([
                self.base_uri,
                '/shared_api/deviation/group_folders',
                query_string({'groupid': group_id, 'type': 'gallery'}),
            ]),
            cookies=self.cookies,
            headers=headers,
        )

        folder_data = validate_response_succeeds(response)
        return [Folder(folder) for folder in folder_data['results']]

    def get_deviation_tags(self, deviation_url):
        """Get list of tags for the provided deviation_id.

        Args:
            deviation_url (str): Deviation URL.

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
        rjson = validate_response_succeeds(response)
        deviation_extended_result = DeviationExtendedResult(rjson)
        return deviation_extended_result.deviation.get_tag_names()

    def add_deviation_to_group(self, group_id, folder_id, deviation_url):
        """Submit deviation to the specified folder in group.

        Args:
            group_id (int): Group ID.
            folder_id (int): Folder ID.
            deviation_url (str): Deviation URL.

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

        rjson = validate_response_succeeds(response)
        if rjson['needsVote']:
            return '✅ Deviation added to folder and automatically approved'
        return '⌛ Deviation submitted to folder and pending mod approval'

    def post_status(self, deviation_url, html_content):
        """Create a status to sta.sh and publish from sta.sh to DeviantArt.

        Args:
            deviation_url (str): Deviation URL, just for CSRF purposes.
            html_content (str): Text content of message in HTML-format.

        Returns:
            string: Success message of result.
        """
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.deviantart.com',
            'referer': deviation_url,
        }
        csrf_token = get_csrf(deviation_url, self.cookies)
        payload = json.dumps({
            'csrf_token': csrf_token,
            'editorRaw': json.dumps(html_to_draftjs(html_content)),
        })
        # POST /status/create creates a sta.sh post from the provided payload.
        response = requests.post(
            ''.join([
                self.base_uri,
                '/shared_api/status/create',
            ]),
            cookies=self.cookies,
            headers=headers,
            data=payload,
        )
        rjson = validate_response_succeeds(response)

        # statusid is the sta.sh ID, not the production DeviantArt status ID.
        payload = json.dumps({
            'csrf_token': csrf_token,
            'statusid': rjson['deviation'].get('deviationId'),
        })
        # POST /status/publish moves the status from sta.sh to DeviantArt.
        response = requests.post(
            ''.join([
                self.base_uri,
                '/shared_api/status/publish',
            ]),
            cookies=self.cookies,
            headers=headers,
            data=payload,
        )
        rjson = validate_response_succeeds(response)
        return '✅ Status created: {0}'.format(rjson['deviation'].get('url'))

    def get_user_comments(self, username, offset, limit=49):
        """Return a paginated call for 5 of the user's recent comments.

        Args:
            username (str): DeviantArt username of user.
            offset (int): Offset to start with API call.
            limit (int, optional): Limit of results to return. Defaults to 49.

        Returns:
            UsersCommentsList: UsersCommentsList instance.

        Raises:
            ValueError: If `limit` is greater than 49.
        """
        # Note: this endpoint's behavior seems to be that it'll only return the
        # 49 most recent comments associated with a particular user account.
        if limit > 49:  # noqa: WPS432
            raise ValueError('Limit must be equal to or below 49.')

        queries = {
            'username': username,
            'moduleid': self.get_module_id(username, 'my_comments'),
            'offset': offset,
            'limit': limit,
        }
        response = requests.get(
            ''.join([
                self.base_uri,
                '/da-user-profile/api/module/my_comments',
                query_string(queries),
            ]),
            cookies=self.cookies,
        )
        rjson = validate_response_succeeds(response)
        return UsersCommentsList(rjson)

    def get_module_id(self, username, module_name):
        """Return module ID for given module name associated with user.

        Args:
            username (str): DeviantArt username of user.
            module_name (str): User profile module name.

        Returns:
            int: Module ID for the module_name.

        Raises:
            RuntimeError: If module with module_name not found.
        """
        queries = {
            'username': username,
        }
        response = requests.get(
            ''.join([
                self.base_uri,
                '/da-user-profile/api/init/about',
                query_string(queries),
            ]),
            cookies=self.cookies,
        )
        rjson = validate_response_succeeds(response)
        # For now, for simplicity, the result of this API call will not be
        # loaded into a model due to how much data gets returned.
        for module in rjson.get('sectionData').get('modules'):
            if module.get('name') == module_name:
                return module.get('id')
        raise RuntimeError("module '{0}' not found.".format(module_name))


def get_deviation_id(deviation_url):
    """Extract the deviation_id from the full deviantart image URL.

    Args:
        deviation_url (str): Deviation URL.

    Returns:
        string: Deviation ID.
    """
    url_parts = deviation_url.split('-')
    return url_parts[-1]


def get_username_from_url(deviation_url):
    """Regex parse deviation URL to retrieve username.

    Args:
        deviation_url (str): Deviation URL.

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
        deviation_url (str): Deviation URL.
        cookies (http.cookiejar.CookieJar): .deviantart.com Cookie Jar.

    Returns:
        string: CSRF validation token.

    Raises:
        RuntimeError: Unable to retrieve CSRF token from provided URL.
    """
    page = requests.get(deviation_url, cookies=cookies)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Check for <input type="hidden" name="validate_token" value="CSRF" />.
    csrf_element = soup.find('input', {'name': 'validate_token'})
    if csrf_element is not None:
        return csrf_element.get('value')

    # Check for window.__CSRF_TOKEN__ = 'CSRF';.
    window_csrf_regex = "window.__CSRF_TOKEN__ = '(.*)';"
    text = soup.find_all(text=re.compile(window_csrf_regex))
    if text:
        csrf_element = re.search(window_csrf_regex, text[0])
        if csrf_element is not None:
            return csrf_element.group(1)

    raise RuntimeError('Unable to retrieve CSRF token from provided URL.')


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


def validate_response_succeeds(response):
    """Check if response returned error, otherwise return dictified response.

    Args:
        response (Response): Response object.

    Returns:
        dict: JSON response as dictionary.
    """
    if response.status_code == http.client.INTERNAL_SERVER_ERROR:
        raise_error(response.reason)
    response_dict = json.loads(response.text)
    if 'error' in response_dict:
        raise_error(response_dict)
    return response_dict


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
