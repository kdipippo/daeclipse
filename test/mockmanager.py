"""Helper class to return mocks for specific fields."""

import json

import responses

import daeclipse


class MockManager(object):
    """Helper class to return mocks for specific fields."""

    http_ok = 200

    def __init__(self):
        """Initialize helper class to return mocks for specific fields."""
        with open('test/mocks/mock_fields.json') as json_file:
            self.fields = json.load(json_file)

    def mock_field(self, field_name):
        """Return mock value for specified field name.

        Args:
            field_name (str): Field name in mock_fields.json.

        Returns:
            any: Value for field name in mock_fields.json.
        """
        return self.fields.get(field_name)

    def url(self, query_name):
        """Return URL for given API call query.

        Args:
            query_name (str): API query name.

        Returns:
            str: API query URL.
        """
        return '{0}/_napi/{1}'.format(
            self.mock_field('base_uri'),
            self.mock_field('api_urls').get(query_name),
        )

    def body(self, mock_name):
        """Return mock from specified JSON file.

        Args:
            mock_name (string): JSON filename in mocks/ folder.

        Returns:
            dict: Dictionary with JSON contents.
        """
        with open('test/mocks/api/{0}.json'.format(mock_name)) as json_file:
            return json.load(json_file)

    def mock_get(self, mock_name, mock_body=None):
        """Mock DeviantArt Eclipse API GET call.

        Args:
            mock_name (str): API query name.
            mock_body (str): mocks/ JSON filename, if different from mock_name.
        """
        if mock_body is None:
            mock_body = mock_name
        responses.add(
            method=responses.GET,
            url=self.url(mock_name),
            json=self.body(mock_body),
            status=self.http_ok,
            match_querystring=False,
        )

    def mock_post(self, mock_name, mock_body=None):
        """Mock DeviantArt Eclipse API POST call.

        Args:
            mock_name (str): API query name.
            mock_body (str): mocks/ JSON filename, if different from mock_name.
        """
        if mock_body is None:
            mock_body = mock_name
        responses.add(
            method=responses.POST,
            url=self.url(mock_name),
            json=self.body(mock_body),
            status=self.http_ok,
            match_querystring=False,
        )

    def mock_user_init_about(self):
        """Mock user_init_about."""
        self.mock_call('GET', 'user_init_about')

    def eclipse(self, mocker):
        """Mock Eclipse with browser_cookie3 and CSRF-fetching disabled.

        Args:
            mocker (MagicMock): Mocker to override code functionality.

        Returns:
            Eclipse: Eclipse instance with cookies and CSRF disabled.
        """
        mocker.patch('browser_cookie3.chrome')
        mocker.patch(
            'daeclipse.api.get_csrf',
            return_value=self.mock_field('csrf'),
        )
        return daeclipse.Eclipse()
