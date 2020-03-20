#!/usr/bin/env python
"""This script provides a way to parse a text file of groups names and update the eclise_groups.json
listing to use with add_art_to_groups.py."""

import json
import sys
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

def sleep_delay(start):
    # wait 10x longer than it took them to respond
    response_delay = int(15 * (time.time() - start))
    print(f"                                 Sleeping {response_delay} seconds")
    time.sleep(response_delay)

if __name__ == "__main__":
    groups_listing_filename = 'eclipse_groups_listing.json'
    with open(groups_listing_filename, 'r') as f:
        groups_listing = json.load(f)

    group_names = read_file_into_words('eclipse_groups_input.txt')
    eclipse = Eclipse()
    count = 0
    for group_name in group_names:
        count += 1
        print(f"{get_percent(count,len(group_names))}% Done - Fetching '{group_name}'")

        t0 = time.time()
        group_id = eclipse.get_group_id(group_name)
        sleep_delay(t0)

        group_info = {
            "group_name": group_name,
            "group_id": group_id,
            "folders": []
        }

        t0 = time.time()
        group_folders = eclipse.get_group_folders(group_id)
        if count != len(group_names):
            sleep_delay(t0)

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

    # groups I want to fetch: pixelized--world, kawaii-explosion

