#!/usr/bin/env python
"""This script takes a deviation url and automatically sends submission requests to groups based
on the category the image falls into."""

from eclipse_api import DeviantArtEclipseAPI as Eclipse

def add_art_to_groups():
    """Reads a deviation URL and adds it to Candycorn-Kingdom's Featured folder."""
    print("Please ensure that the deviation is open in Eclipse in Chrome before continuing.")
    art_url = input("Paste deviation URL: ")
    eclipse = Eclipse()
    eclipse.add_deviation_to_group(
        40852213,      # Candycorn-Kingdom
        60854872,      # Featured
        art_url, # "https://www.deviantart.com/pepper-wood/art/Digital-Inktober-Test-2018-765976537"
    )

if __name__ == "__main__":
    add_art_to_groups()
