#!/usr/bin/env python
"""This script takes a deviation url and automatically sends submission requests to groups based
on the category the image falls into."""

import json
import eclipse_api
import eclipse_groups

def add_art_to_groups():
    """Automatically sends out group submission requests based on a user-provided deviation URL and
    a set of folder categories."""
    print("Please ensure that the deviation is open in Eclipse in Chrome before continuing.")
    art_url = input("Paste deviation URL: ")
    groups_listing = eclipse_groups.Groups()

    # TODO 1) obtain the list of categories
    categories = groups_listing.get_categories()
    # TODO 2) send out a window with checkbox options to submit
    # TODO 3) receive the list of checkbox selections
    # TODO 4) use the checkbox selections to get the list of groups & folders to submit to
    # TODO 5) iterate over result with add_deviation_to_group. Be sure that this call shows with delays.

    '''
    eclipse = eclipse_api.Eclipse()
    eclipse.add_deviation_to_group(
        40852213,      # Candycorn-Kingdom
        60854872,      # Featured
        art_url, # "https://www.deviantart.com/pepper-wood/art/Digital-Inktober-Test-2018-765976537"
    )
    '''

if __name__ == "__main__":
    add_art_to_groups()
