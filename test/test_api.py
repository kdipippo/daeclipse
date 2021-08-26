"""Test to cover Eclipse class API call methods."""  # noqa: WPS226

from test.mockmanager import MockManager

import pytest
import responses

MOCK = MockManager()
USERNAME = MOCK.mock_field('username')
DEVIATION_URL = MOCK.mock_field('deviation_url')


@responses.activate
def test_get_groups(mocker):
    """Test get_groups().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    MOCK.mock_user_init_about()
    MOCK.mock_get('user_group_members')

    actual = MOCK.eclipse(mocker).get_groups(USERNAME, 0)
    expected_names = ['ExampleGroup1', 'ExampleGroup2']
    assert len(actual.groups) == len(expected_names)
    for index, group in enumerate(actual.groups):
        assert group.username == expected_names[index]


@responses.activate
def test_get_group_folders(mocker):
    """Test get_group_folders().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    MOCK.mock_get('group_folders')

    actual = MOCK.eclipse(mocker).get_group_folders(
        MOCK.mock_field('group_id'),
        DEVIATION_URL,
    )
    expected_names = ['Featured']
    assert len(actual) == len(expected_names)
    for index, folder in enumerate(actual):
        assert folder.name == expected_names[index]


@responses.activate
def test_get_deviation_tags(mocker):
    """Test get_deviation_tags().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    MOCK.mock_get('extended_fetch')

    actual = MOCK.eclipse(mocker).get_deviation_tags(DEVIATION_URL)
    expected = ['exampletag', 'exampletag2']
    assert len(actual) == len(expected)
    assert actual == expected


@responses.activate
def test_add_deviation_to_group(mocker):
    """Test add_deviation_to_groups().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    MOCK.mock_post('group_add')

    actual = MOCK.eclipse(mocker).add_deviation_to_group(
        MOCK.mock_field('group_id'),
        MOCK.mock_field('folder_id'),
        DEVIATION_URL,
    )
    expected = '⌛ Deviation submitted to folder and pending mod approval'
    assert actual == expected


@responses.activate
def test_post_status(mocker):
    """Test post_status().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    MOCK.mock_post('status_create', 'status_create_or_publish')
    MOCK.mock_post('status_publish', 'status_create_or_publish')

    eclipse = MOCK.eclipse(mocker)
    actual = eclipse.post_status(
        DEVIATION_URL,
        MOCK.mock_field('html_content'),
    )
    expected = '✅ Status created: {0}'.format(DEVIATION_URL)
    assert actual == expected


@responses.activate
def test_get_user_comments(mocker):
    """Test get_user_comments().

    Args:
        mocker (MagicMock): Mocker to override code functionality.
    """
    MOCK.mock_user_init_about()
    MOCK.mock_get('user_my_comments')

    actual = MOCK.eclipse(mocker).get_user_comments(USERNAME)
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
    MOCK.mock_user_init_about()

    eclipse = MOCK.eclipse(mocker)
    expected_modules = [
        ('watchers', 1709114043),
        ('group_list_members', 1709114041),
    ]
    for expected_module in expected_modules:
        assert expected_module[1] == eclipse.get_module_id(
            USERNAME,
            expected_module[0],
        )

    with pytest.raises(Exception) as execinfo:
        eclipse.get_module_id(USERNAME, 'nonexistent')
        assert execinfo.value.args[0] == "module 'nonexistent' not found."
        assert str(execinfo.value) == "module 'nonexistent' not found."
