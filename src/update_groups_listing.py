#!/usr/bin/env python
"""This script provides a way to parse a text file of groups names and update the eclise_groups.json
listing to use with add_art_to_groups.py."""

import json
import time
from eclipse_api import DeviantArtEclipseAPI as Eclipse

def read_file_into_words(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

def get_percent(count, total):
    result = count / total
    result *= 100
    result = int(result)
    return result

if __name__ == "__main__":
    groups_listing_filename = 'eclipse_groups_listing.json'
    with open(groups_listing_filename, 'r') as f:
        groups_listing = json.load(f)

    group_names = read_file_into_words('eclipse_groups_input.txt')
    eclipse = Eclipse()
    count = 0
    for group_name in group_names:
        t0 = time.time()
        count += 1
        print(f"{get_percent(count,len(group_names))}% Done - Fetching '{group_name}'")
        group_id = eclipse.get_group_id(group_name)

        group_info = {
            "group_name": group_name,
            "group_id": group_id,
            "folders": []
        }

        group_folders = eclipse.get_group_folders(group_id)
        if len(group_folders) == 0:
            print("❌ No folders found.")
        for result in group_folders["results"]:
            folder = {
                "folder_name": result["name"],
                "folder_id": result["folderId"],
                "categories": []
            }
            group_info["folders"].append(folder)

        groups_listing["groups_information"].append(group_info)
        response_delay = time.time() - t0
        print(f"                                 {response_delay}")
        time.sleep(10*response_delay)  # wait 10x longer than it took them to respond

    json_file = open(groups_listing_filename, 'w')
    json_file.write(json.dumps(groups_listing, indent=2))
    json_file.close()

    # groups I want to fetch: pixelized--world, kawaii-explosion

