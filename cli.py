"""Main file for building the app into a GUI."""

import datetime
import re

import cli_ui
import dotenv
import json
import typer
import os
from pathlib import Path
from pick import pick
from progress.bar import Bar

import daeclipse
import deviantart
import gif_generator

COLUMN_WIDTH = 25

app = typer.Typer(help='DeviantArt Eclipse CLI')


@app.command()
def gif_preset():
    """Generate pixel icon gif based on a stored preset."""
    presets = gif_generator.get_presets()
    selected_preset = cli_ui.ask_choice(
        'Select which option to generate',
        choices=presets,
        sort=False,
    )
    gif_filename = gif_generator.create_gif_preset(selected_preset)
    cli_ui.info('Generated pixel icon created at', gif_filename)


@app.command()
def gif_random():
    """Generate pixel icon gif with randomized assets."""
    gif_filename = gif_generator.create_gif_random()
    cli_ui.info('Generated pixel icon created at', gif_filename)


@app.command()
def add_art_to_groups(  # noqa: WPS210
    save: bool = typer.Option(  # noqa: B008, WPS404
        False,  # noqa: WPS425
        help='Save results to local file.',
    ),
):
    """Submit DeviantArt deviation to groups.

    Args:
        save (bool): --save to save to local file. Defaults to False.
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
    dotenv_file = dotenv.find_dotenv()
    if dotenv_file == '':
        cli_ui.error(".env file not found. Creating a blank one now.")
        Path('.env').touch()
        dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    client_id = os.getenv('deviantart_client_id')
    client_secret = os.getenv('deviantart_client_secret')

    if client_id is None or client_secret is None:
        cli_ui.info_1("Retrieve public API credentials at", cli_ui.underline, cli_ui.bold, "https://www.deviantart.com/developers/apps", cli_ui.reset)

    if client_id is None:
        cli_ui.error("Missing deviantart_client_id")
        client_id = cli_ui.ask_password('Enter your dA client ID:')
        dotenv.set_key(dotenv_file, "deviantart_client_id", client_id)

    if client_secret is None:
        cli_ui.error("Missing deviantart_client_secret")
        client_secret = cli_ui.ask_password('Enter your dA client secret:')
        dotenv.set_key(dotenv_file, "deviantart_client_secret", client_secret)
    return deviantart.Api(client_id, client_secret)

@app.command()
def get_tags():
    """Return list of tags for given deviation."""
    eclipse = daeclipse.Eclipse()
    deviation_url = cli_ui.ask_string('Paste deviation URL:   ')
    tags = eclipse.get_deviation_tags(deviation_url)
    cli_ui.info_1(tags)

@app.command()
def hot_tags(
    save: bool = typer.Option(  # noqa: B008, WPS404
        False,  # noqa: WPS425
        help='Save results to local file.',
    ),
):
    """Return top 10 tags on the 100 hottest deviations."""
    eclipse = daeclipse.Eclipse()  # Internal Eclipse API wrapper.
    da = initialize_deviantart()  # Public API wrapper.
    popular_count = 100
    popular = da.browse(endpoint='popular', limit=popular_count)
    deviations = popular['results']
    popular_tags = {}
    bar = Bar('Parsing 100 hottest deviations', max=popular_count)
    for deviation in deviations:
        bar.next()
        tags = eclipse.get_deviation_tags(deviation.url)
        for tag in tags:
            if tag not in popular_tags:
                popular_tags[tag] = 1
            else:
                popular_tags[tag] += 1
    cli_ui.info()
    popular_tags = sorted(popular_tags.items(), key=lambda x: x[1], reverse=True)
    top_10_tags = popular_tags[0:10]
    tag_table = [[(cli_ui.bold, i[0]), (cli_ui.green, i[1])] for i in top_10_tags]
    cli_ui.info_table(tag_table, headers=['tag', 'count'])
    if save:
        with open("popular_tags.json", "w") as outfile: 
            json.dump(popular_tags, outfile)


def get_username_from_url(deviation_url):
    """Regex parse deviation URL to retrieve username.

    Args:
        deviation_url (string): Deviation URL.

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
        group (EclipseGruser): EclipseGruser object representing group.
        deviation_url (string): Deviation URL.

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
        group_name (string): Group name.
        folder_name (string): Folder name.
        message (string): Status message.

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
