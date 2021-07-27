"""Main file for building the app into a GUI."""

import cli_ui
import datetime
import re
import typer
from pick import pick

import eclipse_api
import gif_generator

app = typer.Typer(help='DeviantArt Eclipse CLI')


@app.command()
def gif_preset():
    """Generate an animated pixel icon gif based on a stored preset."""
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
    """Generate an animated pixel icon gif with randomized assets."""
    gif_filename = gif_generator.create_gif_random()
    cli_ui.info('Generated pixel icon created at', gif_filename)


@app.command()
def add_art_to_groups(
    save: bool = typer.Option(False, help="Save results to local file."),
):
    """Submit DeviantArt deviation to groups."""
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

    eclipse = eclipse_api.Eclipse()
    offset = 0
    while True:
        groups = eclipse.get_groups(da_username, offset)
        offset = groups['nextOffset']

        selected_groups = pick(
            get_group_names(groups['results']),
            ' '.join([
                'Select which groups to submit your art (press SPACE to mark,',
                'ENTER to continue): ',
            ]),
            multiselect=True,
        )

        for selected_group in selected_groups:
            status, message = handle_selected_group(
                eclipse,
                selected_group[0],
                groups['results'][selected_group[1]]['userId'],
                deviation_url,
            )
            if status:
                cli_ui.info(message)
            else:
                cli_ui.info(cli_ui.red, message, cli_ui.reset)
            if save:
                with open('eclipse_{0}.txt'.format(curr_time), 'a') as sfile:
                    sfile.write("{0}\n".format(message))

        if not groups['hasMore']:
            return


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


def get_group_names(groups):
    """Return list of group names from list of dicts.

    Args:
        groups (dict[]): List of dicts containing group information.

    Returns:
        string[]: List of group names.
    """
    group_names = [group['username'] for group in groups]
    group_names.sort(key=str.lower)
    return group_names


def get_folder_names(folders):
    """Return list of folder names from list of EclipseFolder objects.

    Args:
        folders (EclipseFolder[]): List of EclipseFolder objects.

    Returns:
        string[]: List of folder names.
    """
    folder_names = [folder.name for folder in folders]
    folder_names.sort(key=str.lower)
    return folder_names


def handle_selected_group(eclipse, group_name, group_id, deviation_url):
    """Submit DeviantArt deviation to group and return response.

    Args:
        eclipse (Eclipse): Eclipse API class instance.
        group_name (string): Group name.
        group_id (int): Group ID.
        deviation_url (string): Deviation URL.

    Returns:
        boolean, string: success status and result message.
    """
    try:
        folders_result = eclipse.get_group_folders(group_id, deviation_url)
    except RuntimeError as folders_rerror:
        return False, format_msg(group_name, '', str(folders_rerror))

    if not folders_result:
        return False, format_msg(group_name, '', 'No folders returned')

    picked_name, picked_index = pick(
        get_folder_names(folders_result),
        ' '.join([
            'Select which folder in "{0}" to add your artwork into',
            '(ENTER to continue): ',
        ]).format(group_name),
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
            group_name,
            picked_name,
            '❌ ' + str(add_art_rerror),
        )

    return True, format_msg(group_name, picked_name, message)


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
        group_name.ljust(25),  # Max-length of username is 20 characters.
        folder_name[:24].ljust(25),
        message,
    )


if __name__ == '__main__':
    app()
