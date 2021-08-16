import json
import responses
import daeclipse


class Mocks(object):
    """Helper class to return mocks for specific fields."""

    HTTP_OK = 200

    def __init__(self):
        """Initialize helper class to return mocks for specific fields."""
        self.base_uri = 'https://www.deviantart.com'
        self.api_urls = {
            'user_init_about': 'da-user-profile/api/init/about',
            'user_group_members': 'da-user-profile/api/module/groups/members',
            'user_my_comments': 'da-user-profile/api/module/my_comments',
            'group_folders': 'shared_api/deviation/group_folders',
            'extended_fetch': 'shared_api/deviation/extended_fetch',
            'group_add': 'shared_api/deviation/group_add',
            'status_create': 'shared_api/status/create',
            'status_publish': 'shared_api/status/publish',
        }

    def url(self, query_name):
        """Return URL for given API call query.

        Args:
            query_name (str): API query name.

        Returns:
            str: API query URL.
        """
        return '{0}/_napi/{1}'.format(self.base_uri, self.api_urls.get(query_name))

    def username(self):
        """Return mock for username field.

        Returns:
            str: Mock for username field.
        """
        return 'ExampleUsername'

    def deviation_url(self):
        """Return mock for deviation_url field.

        Returns:
            str: Mock for username field.
        """
        return '{0}/{1}/art/example-artwork-12345'.format(
            self.base_uri,
            self.username,
        )

    def id(self):
        """Return mock for ID field.

        Returns:
            int: Mock for ID field.
        """
        return 12345678

    def group_id(self):
        """Return mock for ID field.

        Returns:
            int: Mock for ID field.
        """
        return 12345678

    def folder_id(self):
        """Return mock for ID field.

        Returns:
            int: Mock for ID field.
        """
        return 12345678

    def csrf(self):
        """Return mock for csrf token.

        Returns:
            str: Mock for csrf token.
        """
        return 'AbCdEfGhIjKlMnOp.QrStUv.WxYzAbCdEfGhIjKlMnOpAbCd_EfGhIjKlMnOpQrStUv'

    def html_content(self):
        """Return mock for html_content field.

        Returns:
            str: Mock for html_content field.
        """
        return 'This is a <b>test message</b> to be sent into a <i>status</i>.'

    def body(self, mock_name):
        """Return mock from specified JSON file.

        Args:
            mock_name (string): JSON filename in mocks/ folder.

        Returns:
            dict: Dictionary with JSON contents.
        """
        with open('test/mocks/{0}.json'.format(mock_name)) as json_file:
            return json.load(json_file)

    def mock_call(self, method, mock_name):
        if method == 'GET':
            responses.add(
                method=responses.GET,
                url=self.url(mock_name),
                json=self.body(mock_name),
                status=self.HTTP_OK,
                match_querystring=False,
            )
        elif method == 'POST':
            responses.add(
                method=responses.POST,
                url=self.url(mock_name),
                json=self.body(mock_name),
                status=self.HTTP_OK,
                match_querystring=False,
            )

    def mock_user_init_about(self):
        self.mock_call('GET', 'user_init_about')
    def mock_user_group_members(self):
        self.mock_call('GET', 'user_group_members')
    def mock_group_folders(self):
        self.mock_call('GET', 'group_folders')
    def eclipse(self, mocker):
        mocker.patch('browser_cookie3.chrome')
        return daeclipse.Eclipse()
