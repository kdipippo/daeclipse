#!/usr/bin/env python
"""This script provides a way to parse a text file of groups names and update the
eclipse_groups.json listing."""

import json
import sys
import eclipse_api
import eclipse_groups


def read_file_into_words(filename):
    """Parses a .txt file and returns each line as an entry in a list.

    Args:
        filename (string): Filename based on relative path.

    Returns:
        list: List of strings.
    """
    with open(filename) as file:
        content = file.readlines()
    content = [x.strip() for x in content]
    return content


def get_percent(count, total):
    """Return the percentage of how many groups have been parsed in the full input .txt file.

    Args:
        count (int): Current count.
        total (int): Total.

    Returns:
        int: Rounded-down percentage.
    """
    result = count / total
    result *= 100
    result = int(result)
    return result


def add_group_to_group_listing(eclipse, group_name, groups_listing) -> None:
    """Takes in a group_name and adds it and its folders to the groups_listing, with a default
    'UNSELECTED' category set.

    Args:
        eclipse (Eclipse): Eclipse API class.
        group_name (string): DeviantArt group name to extract information from.
        groups_listing (Groups): Groups class.
    """
    group_id = eclipse_api.get_group_id(group_name)

    group_info = {
        "group_name": group_name,
        "group_id": group_id,
        "folders": []
    }
    group_folders = eclipse.get_group_folders(group_id)

    if "errors" in group_folders:
        print(json.dumps(group_folders))
        sys.exit(1)
    if len(group_folders["results"]) == 0:
        print("❌ No folders found.")
        print(json.dumps(group_folders))
    for result in group_folders["results"]:
        folder = {
            "folder_name": result["name"],
            "folder_id": result["folderId"],
            "category": "UNSELECTED"
        }
        group_info["folders"].append(folder)

    groups_listing.add_group(group_info)


def update_groups_listing():
    """Update the eclipse_groups_listing.json file with groups and their folders based on what is
    currently listed to parse in eclipse_groups_input.txt"""
    groups_listing = eclipse_groups.Groups()
    eclipse = eclipse_api.Eclipse()

    groups_input_filename = input("[FILE INPUT] Specify the .txt file containing the new groups.")
    group_names = read_file_into_words(groups_input_filename)
    count = 0
    for group_name in group_names:
        count += 1
        print(f"{get_percent(count,len(group_names))}% Done - Fetching '{group_name}'")
        add_group_to_group_listing(eclipse, group_name, groups_listing)


if __name__ == "__main__":
    update_groups_listing()
