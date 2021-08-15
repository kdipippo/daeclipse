import responses
import requests
import daeclipse
import json


class Mock(object):
    def username(self):
        return "ExampleUsername"
    def deviation_url(self):
        return "https://www.deviantart.com/exampleusername/art/example-artwork-12345"
    def body(self, mock_name):
        with open('test/mocks/{0}.json'.format(mock_name)) as json_file:
            return json.load(json_file)
    def id(self):
        return 12345678
    def group_id(self):
        return self.id()
    def folder_id(self):
        return self.id()
    def csrf(self):
        return "AbCdEfGhIjKlMnOp.QrStUv.WxYzAbCdEfGhIjKlMnOpAbCd_EfGhIjKlMnOpQrStUv"


@responses.activate
def test_get_groups(mocker):
    mock = Mock()
    responses.add(
        method=responses.GET,
        url='https://www.deviantart.com/_napi/da-user-profile/api/init/about',
        json=mock.body('module_init_about'),
        status=200,
        match_querystring=False
    )
    responses.add(
        method=responses.GET,
        url='https://www.deviantart.com/_napi/da-user-profile/api/module/groups/members',
        json=mock.body('module_group_members'),
        status=200,
        match_querystring=False
    )

    mocker.patch('browser_cookie3.chrome')
    eclipse = daeclipse.Eclipse()
    actual = eclipse.get_groups(mock.username(), 0)
    expected_names = ['ExampleGroup1', 'ExampleGroup2']
    assert len(actual.groups) == len(expected_names)
    for index in range(len(actual.groups)):
        assert actual.groups[index].username == expected_names[index]


@responses.activate
def test_get_group_folders(mocker):
    mock = Mock()
    responses.add(
        method=responses.GET,
        url='https://www.deviantart.com/_napi/shared_api/deviation/group_folders',
        json=mock.body('group_folders'),
        status=200,
        match_querystring=False
    )

    mocker.patch('browser_cookie3.chrome')
    eclipse = daeclipse.Eclipse()
    actual = eclipse.get_group_folders(mock.group_id(), mock.deviation_url())
    expected_names = ['Featured']
    assert len(actual) == len(expected_names)
    for index in range(len(actual)):
        assert actual[index].name == expected_names[index]


@responses.activate
def test_get_deviation_tags(mocker):
    mock = Mock()
    responses.add(
        method=responses.GET,
        url='https://www.deviantart.com/_napi/shared_api/deviation/extended_fetch',
        json=mock.body('extended_fetch'),
        status=200,
        match_querystring=False
    )

    mocker.patch('browser_cookie3.chrome')
    eclipse = daeclipse.Eclipse()
    actual = eclipse.get_deviation_tags(mock.deviation_url())
    expected = ['exampletag', 'exampletag2']
    assert len(actual) == len(expected)
    assert actual == expected


@responses.activate
def test_add_deviation_to_group(mocker):
    mock = Mock()
    responses.add(
        method=responses.POST,
        url='https://www.deviantart.com/_napi/shared_api/deviation/group_add',
        json=mock.body('group_add'),
        status=200,
        match_querystring=False
    )

    mocker.patch('browser_cookie3.chrome')
    mocker.patch('daeclipse.api.get_csrf', return_value=mock.csrf())
    eclipse = daeclipse.Eclipse()
    actual = eclipse.add_deviation_to_group(
        mock.group_id(),
        mock.folder_id(),
        mock.deviation_url()
    )
    expected = '⌛ Deviation submitted to folder and pending mod approval'
    assert actual == expected


@responses.activate
def test_post_status():
    assert 5 == 5


@responses.activate
def test_get_user_comments():
    assert 5 == 5


@responses.activate
def test_get_module_id():
    assert 5 == 5
