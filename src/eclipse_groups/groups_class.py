#!/usr/bin/env python
"""Class to handle managing the list of DeviantArt Eclipse groups to perform actions against."""

import json
import pathlib


class Groups:
    """Class to handle managing the list of DeviantArt Eclipse groups to perform actions against."""

    base_path = pathlib.Path(__file__).parent.absolute()
    groups_listing_filename = f'{base_path}/eclipse_groups_listing.json'

    def __init__(self):
        with open(self.groups_listing_filename, 'r') as groups_listing_file:
            self.groups = json.load(groups_listing_file)

    def get_categories(self):
        """Return the list of categories assigned to folders.

        Returns:
            list: Alphabetized list of folder category strings.
        """
        categories = []
        for group in self.groups["groups_information"]:
            for folder in group["folders"]:
                if len(folder["category"]) > 0:
                    category_str = folder["category"].replace("(", "").replace(")", "")
                    category_list = category_str.split(" ")
                    for cat in category_list:
                        if cat not in categories and cat not in ["and", "or"]:
                            categories.append(cat)
        categories.sort()
        return categories

    def add_group(self, group_info) -> None:
        """Adds provided group_info dict to the json file and saves.

        Args:
            group_info (dict): Provided group_info dict.
        """
        self.groups["groups_information"].append(group_info)
        self.save_json()

    def save_json(self):
        """Saves the current groups dictionary to eclipse_groups_listing.json."""
        json_file = open(self.groups_listing_filename, 'w')
        json_file.write(json.dumps(self.groups, indent=2))
        json_file.close()

    def go_through_empty_categories(self):
        """Iterates over UNSELECTED folder categories to correctly assign them."""
        print("Leave blank to delete folder")
        for group in self.groups["groups_information"]:
            new_folders = []
            prompt_continue = False
            already_printed = False
            print(f"\n⭐{group['group_name']}")
            for folder in group["folders"]:
                if folder["category"] != "UNSELECTED":
                    new_folders.append(folder)
                else:
                    if not already_printed:
                        for folder_listing in group["folders"]:
                            print(f"-- {folder_listing['folder_name']}")
                        print("-------------------")
                        already_printed = True
                    prompt_continue = True
                    result = input(f"'{folder['folder_name']}'. Category? : ")
                    if result != "":
                        folder["category"] = result
                        new_folders.append(folder)
            group["folders"] = new_folders
            if prompt_continue:
                cont = input("Continue? 'EXIT to leave: ")
                if cont == "EXIT":
                    break
        self.save_json()

    def get_submission_folders(self, checkboxes):
        """Return the list of group ids and corresponding folder ids to submit to based on the
        provided checkbox selections.

        Args:
            checkboxes (dict): Folder categories marked as True or False, i.e. { 'pixel': True }

        Returns:
            list(dict): List of group and folder ids to submit to, as a list of dictionaries.
        """
        checkboxes['all'] = True
        for variable in checkboxes.keys():
            locals()[variable] = checkboxes[variable]
        results = []
        for group in self.groups["groups_information"]:
            folder_id = None
            folder_name = None
            max_query_length = 0
            for folder in group["folders"]:
                folder_query = eval(folder["category"]) # pylint: disable=eval-used
                if folder_query and len(folder["category"]) > max_query_length:
                    folder_id = folder['folder_id']
                    folder_name = folder['folder_name']
                    max_query_length = len(folder["category"])
            if folder_id is not None:
                results.append({
                    "group_id": group["group_id"],
                    "folder_id": folder_id
                })
        return results
