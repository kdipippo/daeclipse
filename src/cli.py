"""Main file for building the app into a GUI."""

import cli_ui
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
def add_art_to_groups():  # noqa: WPS210
    """Submit DeviantArt deviation to groups."""
    da_username = cli_ui.ask_string('Enter DeviantArt username:')
    typer.echo(''.join([
        'Please ensure that the deviation is open in Eclipse in Chrome',
        'before continuing.',
    ]))
    deviation_url = cli_ui.ask_string('Paste deviation URL:')
    eclipse = eclipse_api.Eclipse()
    offset = 0
    while True:
        groups = eclipse.get_groups(da_username, offset)
        offset = groups['nextOffset']

        selected_groups = pick(
            [group['username'] for group in groups['results']].sort(key=str.lower), # TODO - this will be fixed by using models instead.
            ''.join([
                'Select which groups to submit your art (press SPACE to mark,',
                ' ENTER to continue): ',
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
                cli_ui.info(cli_ui.check, message)
            else:
                cli_ui.error(cli_ui.cross, message)

        if not groups['hasMore']:
            return


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
        [folder.name for folder in folders_result].sort(key=str.lower),
        ''.join([
            'Select which folder in "{0}" to add your artwork into ',
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
        return False, format_msg(group_name, picked_name, str(add_art_rerror))

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
    return '{0} | {1} | {2}'.format(group_name, folder_name, message)


if __name__ == '__main__':
    app()
