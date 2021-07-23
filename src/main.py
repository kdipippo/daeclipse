#!/usr/bin/env python
"""Main file for building the app into a GUI."""

# standard imports
import os
import sys
import webbrowser

import cli_ui

# local package imports
import eclipse_api
import eclipse_groups
from gif_generator import create_gif
from update_groups_listing import update_groups_listing, get_percent

import fire

def popup_input(prompt) -> str:
    """Override the input() function when working in the UI, based on what the
    prompt string contains.

    Args:
        prompt (string): Message the user sees when prompted.

    Returns:
        string: user input result.
    """
    if "(Yes/No)" in prompt:
        result = cli_ui.ask_yes_no(prompt)
    elif "[FILE INPUT]" in prompt:
        result = None
        print("ERROR!!!!! this needs to be a function parameter")
    else:
        result = cli_ui.ask_string(prompt)
    return result

class TestCliParentClass:
    def get_folder_categories(self) -> None:
        """Displays the list of categories."""
        groups_listing = eclipse_groups.Groups()
        categories = groups_listing.get_categories()
        for category in categories:
            print(category)


    def populate_empty_folder_categories(self):
        """Pass-through for go_through_empty_categories()."""
        groups_listing = eclipse_groups.Groups()
        groups_listing.go_through_empty_categories()

    def call_create_gif(self):
        """Generate an animated icon gif and open the result as a preview HTML page in the browser."""
        gif_filename = create_gif()
        with open('create_gif_template.html', 'r') as file:
            html = file.read().replace('\n', '')
        html = html.replace("{{gif_filename}}", gif_filename)
        create_gif_result_path = os.path.abspath('create_gif_result.html')
        create_gif_result_url = f"file://{create_gif_result_path}"

        with open(create_gif_result_path, 'w') as create_gif_result:
            create_gif_result.write(html)
        webbrowser.open(create_gif_result_url)


    def get_category_selection(self, categories):
        # TODO - this will break since it's multiple selection
        # BETTER IDEA - pull from user's list of groups and just go one-by-one to submit to groups
        # Even though that's not automated, it can be iterated on later
        return
        """Displays a popup with all possible folder categories to prompt user for appropriate folders.

        Args:
            categories (list(string)): List of folder category names.

        Returns:
            dict(string:boolean): Folder categories marked as True or False, i.e. { 'pixel': True }
        """
        checkbox_layout = []
        checkbox_row = []
        for i in enumerate(categories):
            if i % 5 == 4:
                checkbox_layout.append(checkbox_row)
                checkbox_row = []
            checkbox_row.append(sg.Checkbox(categories[i], key=categories[i]))
        checkbox_layout.append(checkbox_row)
        checkbox_layout.append([sg.Button('SUBMIT'), sg.Button('EXIT')])
        checkbox_window = sg.Window("heyo", checkbox_layout)
        while True:
            checkbox_event, checkbox_values = checkbox_window.Read()
            if checkbox_event in (None, 'EXIT'):
                checkbox_window.Close()
                return dict()
            if checkbox_event == 'SUBMIT':
                checkbox_window.Close()
                print("==== SELECTED ====")
                for checkbox_key in checkbox_values.keys():
                    if checkbox_values[checkbox_key]:
                        print(f"- {checkbox_key}")
                print("==================")
                return checkbox_values


    def add_art_to_groups(self):
        """Automatically sends out group submission requests based on a user-provided deviation URL and
        a set of folder categories."""
        print("Please ensure that the deviation is open in Eclipse in Chrome before continuing.")
        art_url = input("Paste deviation URL: ")
        groups_listing = eclipse_groups.Groups()

        categories = groups_listing.get_categories()
        checkbox_values = get_category_selection(categories)
        submission_folders = groups_listing.get_submission_folders(checkbox_values)
        cont = input("Do you want to move forward with the submission process? (Yes/No): ")
        if cont == "Yes":
            eclipse = eclipse_api.Eclipse()
            count = 0
            for folder in submission_folders:
                print(f"{get_percent(count, len(submission_folders))}% Done - Submitting to Group " +
                    f"{folder['group_id']}, Folder {folder['folder_id']}")
                eclipse.add_deviation_to_group(folder["group_id"], folder["folder_id"], art_url)
                count += 1
        elif cont == "No":
            print("Stopping action.")

    def list(self):
        actions = [
            {
                "func": "call_create_gif",
                "desc": "Generate icon"
            },
            {
                "func": "update_groups_listing",
                "desc": "Add new groups"
            },
            {
                "func": "get_folder_categories",
                "desc": "Get folder categories"
            },
            {
                "func": "populate_empty_folder_categories",
                "desc": "Populate empty folder categories"
            },
            {
                "func": "add_art_to_groups",
                "desc": "Submit art to groups"
            }
        ]
        for action in actions:
            cli_ui.info_1(cli_ui.bold, action['func'].ljust(35), cli_ui.reset, action['desc'])

if __name__ == "__main__":
    fire.Fire(TestCliParentClass)
