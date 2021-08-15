import responses
import requests
import daeclipse
import json
import pytest


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
    def html_content(self):
        return "This is a <b>test message</b> to be sent into a <i>status</i>."


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
def test_post_status(mocker):
    mock = Mock()
    responses.add(
        method=responses.POST,
        url='https://www.deviantart.com/_napi/shared_api/status/create',
        json=mock.body('status_create_or_publish'),
        status=200,
        match_querystring=False
    )
    responses.add(
        method=responses.POST,
        url='https://www.deviantart.com/_napi/shared_api/status/publish',
        json=mock.body('status_create_or_publish'),
        status=200,
        match_querystring=False
    )

    mocker.patch('browser_cookie3.chrome')
    mocker.patch('daeclipse.api.get_csrf', return_value=mock.csrf())
    eclipse = daeclipse.Eclipse()
    actual = eclipse.post_status(
        mock.deviation_url(),
        mock.html_content(),
    )
    expected = '✅ Status created: https://www.deviantart.com/exampleusername/art/Example-Title-112233445'
    assert actual == expected


@responses.activate
def test_get_user_comments(mocker):
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
        url='https://www.deviantart.com/_napi/da-user-profile/api/module/my_comments',
        json=mock.body('module_my_comments'),
        status=200,
        match_querystring=False
    )

    mocker.patch('browser_cookie3.chrome')
    eclipse = daeclipse.Eclipse()
    actual = eclipse.get_user_comments(mock.username())
    assert actual.has_more
    assert actual.next_offset == 10

    actual_comment = actual.comments[0]
    assert actual_comment.get_url() == "https://www.deviantart.com/comments/1/112233445/1234567890"
    assert actual_comment.get_posted_date() == "2021-05-18T12:23:01-0700"
    assert actual_comment.get_text() == 'Great...<span emote=":) ">:) </span><link url="http://spamlink.cf/"/>/'


@responses.activate
def test_get_module_id(mocker):
    mock = Mock()
    responses.add(
        method=responses.GET,
        url='https://www.deviantart.com/_napi/da-user-profile/api/init/about',
        json=mock.body('module_init_about'),
        status=200,
        match_querystring=False
    )

    mocker.patch('browser_cookie3.chrome')
    eclipse = daeclipse.Eclipse()
    assert eclipse.get_module_id(mock.username(), 'watchers') == 1709114043
    assert eclipse.get_module_id(mock.username(), 'group_list_members') == 1709114041
    with pytest.raises(Exception) as execinfo:
        eclipse.get_module_id(mock.username(), 'nonexistent')

    assert execinfo.value.args[0] == "module 'nonexistent' not found."
    assert str(execinfo.value) == "module 'nonexistent' not found."
