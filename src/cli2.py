#!/usr/bin/env python
"""Main file for building the app into a GUI."""

# standard imports
import cli_ui
import os
from pick import pick
import sys
import typer

# local package imports
import eclipse_api
import eclipse_groups
import gif_generator
from update_groups_listing import update_groups_listing, get_percent

app = typer.Typer(help="Awesome CLI user manager.")

@app.command()
def get_folder_categories() -> None:
    """Displays the list of categories."""
    groups_listing = eclipse_groups.Groups()
    categories = groups_listing.get_categories()
    for category in categories:
        typer.echo(category)

@app.command()
def populate_empty_folder_categories():
    """Pass-through for go_through_empty_categories()."""
    groups_listing = eclipse_groups.Groups()
    groups_listing.go_through_empty_categories()

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
    groups_listing = eclipse_groups.Groups()

    categories = groups_listing.get_categories()

    title = "Select which categories your artwork falls under (press SPACE to mark, ENTER to continue): "
    selected_categories = pick(categories, title, multiselect=True, min_selection_count=1)
    # selected_categories is formatted [('all', 1), ('base', 5), ...], so we need to get just the names.
    checkbox_values = ([x[0] for x in selected_categories])

    # Convert the lists of categories into a dict that represents the status of all of them, i.e. { 'pixel': True }.
    checkboxes = {}
    for category in categories:
        checkboxes[category] = False
    for category in selected_categories:
        checkboxes[category] = True

    submission_folders = groups_listing.get_submission_folders(checkboxes)
    cli_ui.info(f"{len(submission_folders)} queued for deviation to be added into.")
    cont = cli_ui.ask_yes_no("Do you want to move forward with the submission process?")
    if not cont:
        cli_ui.info("Stopping action.")
        return
    eclipse = eclipse_api.Eclipse()
    count = 0
    for folder in submission_folders:
        typer.echo(f"{get_percent(count, len(submission_folders))}% Done - Submitting to Group " +
            f"{folder['group_id']}, Folder {folder['folder_id']}")
        eclipse.add_deviation_to_group(folder["group_id"], folder["folder_id"], art_url)
        count += 1

@app.command()
def testing():
    deviation = "https://www.deviantart.com/pepper-wood/art/Gawr-Gura-gif-868331085"
    eclipse = eclipse_api.Eclipse()
    offset = 0
    while True:
        groups_result = eclipse.get_groups("Pepper-Wood", offset)
        offset = groups_result['nextOffset']
        group_names = [group['username'] for group in groups_result['results']]
        group_names.sort()

        title = "Select which groups to add your artwork into (press SPACE to mark, ENTER to continue): "
        selected_groups = pick(group_names, title, multiselect=True, min_selection_count=1)

        for selected_group in selected_groups:
            # ('group name', index)
            selected_group_name = selected_group[0]
            selected_group_index = selected_group[1]
            folders_result = eclipse.get_group_folders(groups_result['results'][selected_group_index]['userId'], deviation)
            print(folders_result)
            return

        if not groups_result['hasMore']:
            return

@app.command()
def list():
    actions = [
        ("call_create_gif", "Generate icon"),
        ("update_groups_listing", "Add new groups"),
        ("get_folder_categories", "Get folder categories"),
        ("populate_empty_folder_categories", "Populate empty folder categories"),
        ("add_art_to_groups", "Submit art to groups"),
    ]
    cli_ui.info("Commands:")
    for action in actions:
        cli_ui.info_1(cli_ui.bold, action[0].ljust(35), cli_ui.reset, action[1])
    cli_ui.info()

if __name__ == "__main__":
    app()
