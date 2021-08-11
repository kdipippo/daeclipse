"""Command to submit DeviantArt deviation to groups."""

import datetime
import re

import cli_ui
import typer
from pick import pick

import daeclipse

COLUMN_WIDTH = 25


def add_art_to_groups(  # noqa: WPS210
    save: bool = typer.Option(  # noqa: B008, WPS404
        False,  # noqa: WPS425
        help='Save results to local file.',
    ),
):
    """Submit DeviantArt deviation to groups.

    Args:
        save (bool): --save to save to local file, defaults to False.
    """
    typer.echo(' '.join([
        'Please ensure that the deviation is open in Eclipse in Chrome',
        'before continuing.',
    ]))
    deviation_url = cli_ui.ask_string('Paste deviation URL:')

    curr_time = datetime.datetime.now()

    try:
        da_username = get_username_from_url(deviation_url)
    except RuntimeError as username_rerror:
        cli_ui.error(str(username_rerror))
        return

    eclipse = daeclipse.Eclipse()
    offset = 0
    while True:
        groups_list = eclipse.get_groups(da_username, offset)
        offset = groups_list.offset
        groups_list.groups.sort(key=lambda group: group.username.lower())

        selected_groups = pick(
            [group.username for group in groups_list.groups],
            ' '.join([
                'Select which groups to submit your art (press SPACE to mark,',
                'ENTER to continue): ',
            ]),
            multiselect=True,
        )

        for selected_group in selected_groups:
            status, message = handle_selected_group(
                eclipse,
                groups_list.groups[selected_group[1]],
                deviation_url,
            )
            if status:
                cli_ui.info(message)
            else:
                cli_ui.info(cli_ui.red, message, cli_ui.reset)
            if save:
                with open('eclipse_{0}.txt'.format(curr_time), 'a') as sfile:
                    sfile.write('{0}\n'.format(message))

        if not groups_list.has_more:
            return


def get_username_from_url(deviation_url):
    """Regex parse deviation URL to retrieve username.

    Args:
        deviation_url (str): Deviation URL.

    Raises:
        RuntimeError: If username is not present in URL string.

    Returns:
        str: DeviantArt username.
    """
    username = re.search('deviantart.com/(.+?)/art/', deviation_url)
    if username:
        return username.group(1)
    raise RuntimeError('DeviantArt username not found in URL.')


def handle_selected_group(eclipse, group, deviation_url):
    """Submit DeviantArt deviation to group and return response.

    Args:
        eclipse (Eclipse): Eclipse API class instance.
        group (Gruser): Gruser object representing group.
        deviation_url (str): Deviation URL.

    Returns:
        boolean, str: success status and result message.
    """
    try:
        folders_result = eclipse.get_group_folders(
            group.user_id,
            deviation_url,
        )
    except RuntimeError as folders_rerror:
        return False, format_msg(group.username, '', str(folders_rerror))

    if not folders_result:
        return False, format_msg(group.username, '', 'No folders returned')

    folders_result.sort(key=lambda folder: folder.name.lower())

    picked_name, picked_index = pick(
        [folder.name for folder in folders_result],
        ' '.join([
            'Select which folder in "{0}" to add your artwork into',
            '(ENTER to continue): ',
        ]).format(group.username),
        multiselect=False,
    )
    folder = folders_result[picked_index]
    try:
        message = eclipse.add_deviation_to_group(
            folder.owner.user_id,
            folder.folder_id,
            deviation_url,
        )
    except RuntimeError as add_art_rerror:
        return False, format_msg(
            group.username,
            picked_name,
            '❌ {0}'.format(str(add_art_rerror)),
        )

    return True, format_msg(group.username, picked_name, message)


def format_msg(group_name, folder_name, message):
    """Return formatted status message for CLI output.

    Args:
        group_name (str): Group name.
        folder_name (str): Folder name.
        message (str): Status message.

    Returns:
        str: Formatted status message containing all arguments.
    """
    return '{0} {1} {2}'.format(
        group_name.ljust(COLUMN_WIDTH),  # Max-length of username is 20 chars.
        folder_name[:(COLUMN_WIDTH - 1)].ljust(COLUMN_WIDTH),
        message,
    )
