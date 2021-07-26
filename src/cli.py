#!/usr/bin/env python
"""Main file for building the app into a GUI."""

import cli_ui
from pick import pick
import typer

import eclipse_api
import gif_generator

app = typer.Typer(help="DeviantArt Eclipse CLI")

@app.command()
def gif_preset():
    """Generate an animated pixel icon gif based on a stored preset."""
    presets = gif_generator.get_presets()
    selected_preset = cli_ui.ask_choice(
        "Select which option to generate",
        choices=presets,
        sort=False
    )
    gif_filename = gif_generator.create_gif_preset(selected_preset)
    cli_ui.info("Generated pixel icon created at", gif_filename)

@app.command()
def gif_random():
    """Generate an animated pixel icon gif with randomized assets."""
    gif_filename = gif_generator.create_gif_random()
    cli_ui.info("Generated pixel icon created at", gif_filename)

@app.command()
def add_art_to_groups():
    """Submit DeviantArt deviation to groups."""
    da_username = cli_ui.ask_string("Enter DeviantArt username:")
    typer.echo("Please ensure that the deviation is open in Eclipse in Chrome before continuing.")
    deviation_url = cli_ui.ask_string("Paste deviation URL:")
    eclipse = eclipse_api.Eclipse()
    offset = 0
    while True:
        groups_result = eclipse.get_groups(da_username, offset)
        offset = groups_result['nextOffset']
        group_names = [group['username'] for group in groups_result['results']]
        group_names.sort()

        title = "Select which groups to submit your art (press SPACE to mark, ENTER to continue): "
        selected_groups = pick(group_names, title, multiselect=True)

        for selected_group in selected_groups:
            status, message = handle_selected_group(
                eclipse,
                selected_group[0],
                groups_result['results'][selected_group[1]]['userId'],
                deviation_url
            )
            if status:
                cli_ui.info(cli_ui.check, message)
            else:
                cli_ui.error(cli_ui.cross, message)

        if not groups_result['hasMore']:
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
    except RuntimeError as runtime_error:
        return False, f"{group_name} | | {str(runtime_error)}"

    if len(folders_result) == 0:
        return False, f"{group_name} | | No folders returned for group"
    folder_names = [folder.name for folder in folders_result]
    title = f"Select which folder in '{group_name}' to add your artwork into (ENTER to continue): "
    selected_folder = pick(folder_names, title, multiselect=False)
    selected_folder_name = selected_folder[0]
    selected_folder_index = selected_folder[1]
    folder = folders_result[selected_folder_index]
    try:
        message = eclipse.add_deviation_to_group(
            folder.owner.user_id,
            folder.folder_id,
            deviation_url
        )
    except RuntimeError as runtime_error:
        return False, f"{group_name} | {selected_folder_name} | {str(runtime_error)}"

    return True, f"{group_name} | {selected_folder_name} | {message}"

if __name__ == "__main__":
    app()
