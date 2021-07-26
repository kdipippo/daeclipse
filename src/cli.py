#!/usr/bin/env python
"""Main file for building the app into a GUI."""

# standard imports
import cli_ui
from pick import pick
import typer

# local package imports
import eclipse_api
import gif_generator

app = typer.Typer(help="DeviantArt Eclipse CLI")

@app.command()
def gif_preset():
    """Generate an animated icon gif based on a stored preset."""
    presets = gif_generator.get_presets()
    selected_preset = cli_ui.ask_choice("Select which option to generate", choices=presets, sort=False)
    gif_filename = gif_generator.create_gif_preset(selected_preset)
    cli_ui.info("Generated pixel icon created at", gif_filename)

@app.command()
def gif_random():
    """Generate an animated icon gif and open the result as a preview HTML page in the browser."""
    gif_filename = gif_generator.create_gif_random()
    cli_ui.info("Generated pixel icon created at", gif_filename)

@app.command()
def add_art_to_groups():
    """Automatically sends out group submission requests based on a user-provided deviation URL and
    a set of folder categories."""
    typer.echo("Please ensure that the deviation is open in Eclipse in Chrome before continuing.")
    art_url = cli_ui.ask_string("Paste deviation URL:")
    eclipse = eclipse_api.Eclipse()
    offset = 0
    while True:
        groups_result = eclipse.get_groups("Pepper-Wood", offset)
        offset = groups_result['nextOffset']
        group_names = [group['username'] for group in groups_result['results']]
        group_names.sort()

        title = "Select which groups to add your artwork into (press SPACE to mark, ENTER to continue): "
        selected_groups = pick(group_names, title, multiselect=True)

        if len(selected_groups) > 0:
            for selected_group in selected_groups:
                # ('group name', index)
                selected_group_name = selected_group[0]
                selected_group_index = selected_group[1]
                folders_result = eclipse.get_group_folders(groups_result['results'][selected_group_index]['userId'], deviation_url)
                if len(folders_result) == 0:
                    cli_ui.error(cli_ui.cross, f"{selected_group_name} | | No folders returned for group")
                else:
                    folder_names = [folder.name for folder in folders_result]
                    title = f"Select which folder in '{selected_group_name}' to add your artwork into (ENTER to continue): "
                    selected_folder = pick(folder_names, title, multiselect=False)
                    selected_folder_name = selected_folder[0]
                    selected_folder_index = selected_folder[1]
                    folder_go = folders_result[selected_folder_index]
                    folder_status, folder_message = eclipse.add_deviation_to_group(folder_go.owner.userId, folder_go.folderId, deviation_url)
                    if folder_status:
                        cli_ui.info(cli_ui.check, f"{selected_group_name} | {selected_folder_name} | {folder_message}")
                    else:
                        cli_ui.error(cli_ui.cross, f"{selected_group_name} | {selected_folder_name} | {folder_message}")

        if not groups_result['hasMore']:
            return

@app.command()
def list():
    actions = [
        ("gif-preset", "Generate pixel icon with fixed assets."),
        ("gif-random", "Generate pixel icon with randomized assets."),
        ("add-art-to-groups", "Submit DeviantArt deviation to groups."),
    ]
    cli_ui.info("Commands:")
    for action in actions:
        cli_ui.info_1(cli_ui.bold, action[0].ljust(35), cli_ui.reset, action[1])
    cli_ui.info()

if __name__ == "__main__":
    app()
