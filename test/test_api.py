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


@responses.activate
def test_get_groups():
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

    eclipse = daeclipse.Eclipse()
    actual = eclipse.get_groups(mock.username(), 0)
    expected_names = ['ExampleGroup1', 'ExampleGroup2']
    assert len(actual.groups) == len(expected_names)
    for index in range(len(actual.groups)):
        assert actual.groups[index].username == expected_names[index]


@responses.activate
def get_group_folders():
    mock = Mock()
    responses.add(
        method=responses.GET,
        url='https://www.deviantart.com/_napi/shared_api/deviation/group_folders',
        json=mock.body('group_folders'),
        status=200,
        match_querystring=False
    )

    eclipse = daeclipse.Eclipse()
    actual = eclipse.get_group_folders(mock.deviation_url())
    expected_names = ['Featured']
    assert len(actual.groups) == len(expected_names)
    for index in range(len(actual.groups)):
        assert actual[index].name == expected_names[index]


@responses.activate
def test_get_deviation_tags():
    mock = Mock()
    responses.add(
        method=responses.GET,
        url='https://www.deviantart.com/_napi/shared_api/deviation/extended_fetch',
        json=mock.body('extended_fetch'),
        status=200,
        match_querystring=False
    )

    eclipse = daeclipse.Eclipse()
    actual = eclipse.get_deviation_tags(mock.deviation_url())
    expected = ['exampletag', 'exampletag2']
    assert len(actual) == len(expected)
    assert actual == expected


@responses.activate
def add_deviation_to_group():
    pass


@responses.activate
def post_status():
    pass


@responses.activate
def get_user_comments():
    pass


@responses.activate
def get_module_id():
    pass
