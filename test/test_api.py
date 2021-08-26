"""Test to cover Eclipse class API call methods."""

from test.mockmanager import MockManager

import pytest
import responses


@responses.activate
def test_get_groups(mocker):
    """Test get_groups().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    mock = MockManager()
    mock.mock_user_init_about()
    mock.mock_get('user_group_members')

    eclipse = mock.eclipse(mocker)
    actual = eclipse.get_groups(mock.mock_field('username'), 0)
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
    mock = MockManager()
    mock.mock_get('group_folders')

    eclipse = mock.eclipse(mocker)
    actual = eclipse.get_group_folders(
        mock.mock_field('group_id'),
        mock.mock_field('deviation_url'),
    )
    expected_names = ['Featured']
    assert len(actual) == len(expected_names)
    for index in range(len(actual)):
        assert actual[index].name == expected_names[index]


@responses.activate
def test_get_deviation_tags(mocker):
    """Test get_deviation_tags().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    mock = MockManager()
    mock.mock_get('extended_fetch')

    eclipse = mock.eclipse(mocker)
    actual = eclipse.get_deviation_tags(mock.mock_field('deviation_url'))
    expected = ['exampletag', 'exampletag2']
    assert len(actual) == len(expected)
    assert actual == expected


@responses.activate
def test_add_deviation_to_group(mocker):
    """Test add_deviation_to_groups().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    mock = MockManager()
    mock.mock_post('group_add')

    eclipse = mock.eclipse(mocker)
    actual = eclipse.add_deviation_to_group(
        mock.mock_field('group_id'),
        mock.mock_field('folder_id'),
        mock.mock_field('deviation_url'),
    )
    expected = '⌛ Deviation submitted to folder and pending mod approval'
    assert actual == expected


@responses.activate
def test_post_status(mocker):
    """Test post_status().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    mock = MockManager()
    mock.mock_post('status_create', 'status_create_or_publish')
    mock.mock_post('status_publish', 'status_create_or_publish')

    eclipse = mock.eclipse(mocker)
    actual = eclipse.post_status(
        mock.mock_field('deviation_url'),
        mock.mock_field('html_content'),
    )
    expected = '✅ Status created: {0}'.format(mock.mock_field('deviation_url'))
    assert actual == expected


@responses.activate
def test_get_user_comments(mocker):
    """Test get_user_comments().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    mock = MockManager()
    mock.mock_user_init_about()
    mock.mock_get('user_my_comments')

    eclipse = mock.eclipse(mocker)
    actual = eclipse.get_user_comments(mock.mock_field('username'))
    assert actual.has_more
    assert actual.next_offset == 10

    actual_comment = actual.comments[0]
    expected = {
        'url': 'https://www.deviantart.com/comments/1/112233445/1234567890',
        'posted_date': '2021-05-18T12:23:01-0700',
        'text': ''.join(
            [
                'Great...<span emote=":) ">:) ',
                '</span><link url="http://spamlink.cf/"/>/',
            ],
        ),
    }
    assert actual_comment.get_url() == expected.get('url')
    assert actual_comment.get_posted_date() == expected.get('posted_date')
    assert actual_comment.get_text() == expected.get('text')


@responses.activate
def test_get_module_id(mocker):
    """Test get_module_id().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    mock = MockManager()
    mock.mock_user_init_about()

    eclipse = mock.eclipse(mocker)
    assert eclipse.get_module_id(mock.mock_field('username'), 'watchers') == 1709114043
    assert eclipse.get_module_id(mock.mock_field('username'), 'group_list_members') == 1709114041

    with pytest.raises(Exception) as execinfo:
        eclipse.get_module_id(mock.mock_field('username'), 'nonexistent')
        assert execinfo.value.args[0] == "module 'nonexistent' not found."
        assert str(execinfo.value) == "module 'nonexistent' not found."
