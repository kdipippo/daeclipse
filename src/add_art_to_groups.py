#!/usr/bin/env python
"""This script takes a deviation url and automatically sends submission requests to groups based
on the category the image falls into."""

import json
import requests
from bs4 import BeautifulSoup
from eclipse_api import DeviantArtEclipseAPI as Eclipse

if __name__ == "__main__":
    # example: https://www.deviantart.com/pepper-wood/art/Digital-Inktober-Test-2018-765976537
    print("Please ensure that the deviation is open in Eclipse in Chrome before continuing.")
    DEVIATION_URL = input("Paste deviation URL: ")
    DEVIANTART = Eclipse()
    DEVIANTART.add_deviation_to_group(
        40852213, # Candycorn-Kingdom
        60854872, # Featured
        "https://www.deviantart.com/pepper-wood/art/Digital-Inktober-Test-2018-765976537"
    )