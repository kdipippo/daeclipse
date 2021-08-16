import pytest
import requests
import responses

import daeclipse
from test.helpers import Mocks


@responses.activate
def test_get_groups(mocker):
    """Test get_groups().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    mock = Mocks()
    mock.mock_user_init_about()
    mock.mock_user_group_members()

    eclipse = mock.eclipse(mocker)
    actual = eclipse.get_groups(mock.username(), 0)
    expected_names = ['ExampleGroup1', 'ExampleGroup2']
    assert len(actual.groups) == len(expected_names)
    for index in range(len(actual.groups)):
        assert actual.groups[index].username == expected_names[index]


@responses.activate
def test_get_group_folders(mocker):
    """Test get_group_folders().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    mock = Mocks()
    mock.mock_group_folders()

    eclipse = mock.eclipse(mocker)
    actual = eclipse.get_group_folders(mock.group_id(), mock.deviation_url())
    expected_names = ['Featured']
    assert len(actual) == len(expected_names)
    for index in range(len(actual)):
        assert actual[index].name == expected_names[index]

'''
@responses.activate
def test_get_deviation_tags(mocker):
    """Test get_deviation_tags().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    mock = Mocks()
    responses.add(
        method=responses.GET,
        url=mock.url('extended_fetch'),
        json=mock.body('extended_fetch'),
        status=HTTP_OK,
        match_querystring=False,
    )

    mocker.patch('browser_cookie3.chrome')
    eclipse = daeclipse.Eclipse()
    actual = eclipse.get_deviation_tags(mock.deviation_url())
    expected = ['exampletag', 'exampletag2']
    assert len(actual) == len(expected)
    assert actual == expected


@responses.activate
def test_add_deviation_to_group(mocker):
    """Test add_deviation_to_groups().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    mock = Mocks()
    responses.add(
        method=responses.POST,
        url=mock.url('group_add'),
        json=mock.body('group_add'),
        status=HTTP_OK,
        match_querystring=False,
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
    """Test post_status().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    mock = Mocks()
    responses.add(
        method=responses.POST,
        url=mock.url('status_create'),
        json=mock.body('status_create_or_publish'),
        status=HTTP_OK,
        match_querystring=False,
    )
    responses.add(
        method=responses.POST,
        url=mock.url('status_publish'),
        json=mock.body('status_create_or_publish'),
        status=HTTP_OK,
        match_querystring=False,
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
    """Test get_user_comments().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    mock = Mocks()
    responses.add(
        method=responses.GET,
        url=mock.url('user_init_about'),
        json=mock.body('user_init_about'),
        status=HTTP_OK,
        match_querystring=False,
    )
    responses.add(
        method=responses.GET,
        url=mock.url('user_my_comments'),
        json=mock.body('user_my_comments'),
        status=HTTP_OK,
        match_querystring=False,
    )

    mocker.patch('browser_cookie3.chrome')
    eclipse = daeclipse.Eclipse()
    actual = eclipse.get_user_comments(mock.username())
    assert actual.has_more
    assert actual.next_offset == 10

    actual_comment = actual.comments[0]
    assert actual_comment.get_url() == 'https://www.deviantart.com/comments/1/112233445/1234567890'
    assert actual_comment.get_posted_date() == '2021-05-18T12:23:01-0700'
    assert actual_comment.get_text() == 'Great...<span emote=":) ">:) </span><link url="http://spamlink.cf/"/>/'


@responses.activate
def test_get_module_id(mocker):
    """Test get_module_id().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    mock = Mocks()
    responses.add(
        method=responses.GET,
        url=mock.url('user_init_about'),
        json=mock.body('user_init_about'),
        status=HTTP_OK,
        match_querystring=False,
    )

    mocker.patch('browser_cookie3.chrome')
    eclipse = daeclipse.Eclipse()
    assert eclipse.get_module_id(mock.username(), 'watchers') == 1709114043
    assert eclipse.get_module_id(mock.username(), 'group_list_members') == 1709114041
    with pytest.raises(Exception) as execinfo:
        eclipse.get_module_id(mock.username(), 'nonexistent')

    assert execinfo.value.args[0] == "module 'nonexistent' not found."
    assert str(execinfo.value) == "module 'nonexistent' not found."
'''
