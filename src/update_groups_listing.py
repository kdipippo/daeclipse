#!/usr/bin/env python
"""This script provides a way to parse a text file of groups names and update the eclise_groups.json
listing to use with add_art_to_groups.py."""

import json
import sys
import time
from eclipse_api import DeviantArtEclipseAPI as Eclipse
from eclipse_helpers import get_group_id

def read_file_into_words(filename):
    """Parses a .txt file and returns each line as an entry in a list.

    Arguments:
        filename {string} -- Filename based on relative path.

    Returns:
        list -- List of strings.
    """
    with open(filename) as file:
        content = file.readlines()
    content = [x.strip() for x in content]
    return content

def get_percent(count, total):
    """Return the percentage of how many groups have been parsed in the full input .txt file.

    Arguments:
        count {int} -- Current count.
        total {int} -- Total.

    Returns:
        int -- Rounded-down percentage.
    """
    result = count / total
    result *= 100
    result = int(result)
    return result

def sleep_delay(start):
    """Pause the program for 15 times the duration of any call made to DeviantArt.

    Arguments:
        start {float} -- Unix timestamp representing the start time.
    """
    # wait 10x longer than it took them to respond
    response_delay = int(15 * (time.time() - start))
    print(f"                                 Sleeping {response_delay} seconds")
    time.sleep(response_delay)

def update_groups_listing():
    """Update the eclipse_groups_listing.json file with groups and their folders based on what is
    currently listed to parse in eclipse_groups_input.txt"""
    groups_listing_filename = 'eclipse_groups_listing.json'
    with open(groups_listing_filename, 'r') as file:
        groups_listing = json.load(file)

    group_names = read_file_into_words('eclipse_groups_input.txt')
    eclipse = Eclipse()
    count = 0
    for group_name in group_names:
        count += 1
        print(f"{get_percent(count,len(group_names))}% Done - Fetching '{group_name}'")

        start_time = time.time()
        group_id = get_group_id(group_name)
        sleep_delay(start_time)

        group_info = {
            "group_name": group_name,
            "group_id": group_id,
            "folders": []
        }

        start_time = time.time()
        group_folders = eclipse.get_group_folders(group_id)
        if count != len(group_names):
            sleep_delay(start_time)

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
                "categories": []
            }
            group_info["folders"].append(folder)

        groups_listing["groups_information"].append(group_info)
        json_file = open(groups_listing_filename, 'w')
        json_file.write(json.dumps(groups_listing, indent=2))
        json_file.close()

if __name__ == "__main__":
    update_groups_listing()
