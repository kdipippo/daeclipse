"""Main file for DeviantArt Eclipse CLI."""

import collections
import datetime
import os
import re

import cli_ui
import deviantart
import dotenv
import typer
from pick import pick
from progress.bar import Bar

import daeclipse

COLUMN_WIDTH = 25

app = typer.Typer(help='DeviantArt Eclipse CLI')


@app.command()
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


def initialize_deviantart():
    """Initialize public API DeviantArt client. Collect creds if no .env found.

    Returns:
        deviantart.Api: deviantart.Api class instance.
    """
    dotenv_file = dotenv.find_dotenv()
    if dotenv_file == '':
        cli_ui.error('.env file not found. Creating and populating one now.')
        dotenv_file = '.env'
        client_id = None
        client_secret = None
    else:
        dotenv.load_dotenv(dotenv_file)
        client_id = os.getenv('deviantart_client_id')
        client_secret = os.getenv('deviantart_client_secret')

    if client_id is None or client_secret is None:
        cli_ui.info_1(
            'Obtain public API credentials at',
            cli_ui.underline,
            cli_ui.bold,
            'https://www.deviantart.com/developers/apps',
            cli_ui.reset,
        )

    if client_id is None:
        cli_ui.error('Missing deviantart_client_id')
        client_id = cli_ui.ask_password('Enter your dA client ID:')
        dotenv.set_key(dotenv_file, 'deviantart_client_id', client_id)

    if client_secret is None:
        cli_ui.error('Missing deviantart_client_secret')
        client_secret = cli_ui.ask_password('Enter your dA client secret:')
        dotenv.set_key(dotenv_file, 'deviantart_client_secret', client_secret)
    return deviantart.Api(client_id, client_secret)


@app.command()
def show_tags(
    deviation_url: str = typer.Option(  # noqa: B008, WPS404
        '',  # noqa: WPS425
        help='Deviation URL to retrieve tags from.',
    ),
):
    """Return list of tags for given deviation.

    Args:
        deviation_url (str): --deviation_url to specify deviation URL.
    """
    eclipse = daeclipse.Eclipse()
    if not deviation_url:
        deviation_url = cli_ui.ask_string('Paste deviation URL: ')
    tags = eclipse.get_deviation_tags(deviation_url)
    cli_ui.info_1(tags)


@app.command()
def hot_tags(
    tag_count: int = typer.Option(  # noqa: B008, WPS404
        10,  # noqa: WPS425
        help='Number of top tags to return.',
    ),
    hot_count: int = typer.Option(  # noqa: B008, WPS404
        100,  # noqa: WPS425
        help='Number of hot deviations to process.',
    ),
):
    """Return top tags on the hottest deviations.

    Args:
        tag_count (int): --tag-count for number of tag results.
        hot_count (int): --hot-count for number of hot deviations to process.
    """
    eclipse = daeclipse.Eclipse()  # Internal Eclipse API wrapper.

    hottest_deviations = initialize_deviantart().browse(  # Public API wrapper.
        endpoint='popular',  # Popular also returns hottest.
        limit=hot_count,
    ).get('results')
    tags = []
    progressbar = Bar(
        'Parsing {0} hottest deviations'.format(hot_count),
        max=hot_count,
    )
    for deviation in hottest_deviations:
        progressbar.next()
        tags.extend(eclipse.get_deviation_tags(deviation.url))
    tags = collections.Counter(tags).most_common(tag_count)

    cli_ui.info()
    cli_ui.info_table(
        [
            [(cli_ui.bold, tag[0]), (cli_ui.green, tag[1])] for tag in tags
        ],
        headers=['tag', 'count'],
    )


@app.command()
def post_status():
    """Post a DeviantArt status."""
    eclipse = daeclipse.Eclipse()
    cli_ui.info_1('Deviation URL is required for CSRF token authorization.')
    deviation_url = cli_ui.ask_string('Paste deviation URL: ')
    status_content = cli_ui.ask_string('Enter HTML-formatted status text: ')

    try:
        status_result = eclipse.post_status(deviation_url, status_content)
    except RuntimeError as status_error:
        cli_ui.error(str(status_error))
    cli_ui.info(status_result)


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


def handle_selected_group(eclipse, group, deviation_url):
    """Submit DeviantArt deviation to group and return response.

    Args:
        eclipse (Eclipse): Eclipse API class instance.
        group (Gruser): Gruser object representing group.
        deviation_url (str): Deviation URL.

    Returns:
        boolean, string: success status and result message.
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
        string: Formatted status message containing all arguments.
    """
    return '{0} {1} {2}'.format(
        group_name.ljust(COLUMN_WIDTH),  # Max-length of username is 20 chars.
        folder_name[:(COLUMN_WIDTH - 1)].ljust(COLUMN_WIDTH),
        message,
    )


if __name__ == '__main__':
    app()
