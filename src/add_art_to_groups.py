#!/usr/bin/env python
"""This script takes a deviation url and automatically sends submission requests to groups based
on the category the image falls into."""

import json
import eclipse_api

def add_art_to_groups():
    """Automatically sends out group submission requests based on a user-provided deviation URL and
    a set of folder categories."""
    print("Please ensure that the deviation is open in Eclipse in Chrome before continuing.")
    art_url = input("Paste deviation URL: ")
    with open('eclipse_groups_listing.json', 'r') as f:
        eclipse_groups_listing = json.load(f)

    eclipse = eclipse_api.Eclipse()
    eclipse.add_deviation_to_group(
        40852213,      # Candycorn-Kingdom
        60854872,      # Featured
        art_url, # "https://www.deviantart.com/pepper-wood/art/Digital-Inktober-Test-2018-765976537"
    )

if __name__ == "__main__":
    add_art_to_groups()
