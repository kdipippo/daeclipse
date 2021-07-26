#!/usr/bin/env python
"""Helper file containing HTML parsing functions for using Eclipse API methods."""

import time
import requests
from bs4 import BeautifulSoup

def get_csrf(deviation_url, cookies):
    """Parses the HTML of the deviation to get the csrf token in the page. It's stored as the
    value of a hidden input with name 'validate_token'.

    Args:
        deviation_url (string): deviation URL, i.e. https://da.com/art/Art-12345.
        cookie (http.cookiejar.CookieJar): .deviantart.com Cookie Jar.

    Returns:
        string: CSRF validation token.
    """
    page = requests.get(deviation_url, cookies=cookies)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup.find("input", {"name":"validate_token"})["value"]

def get_group_id(group_name):
    """Parses the HTML of a DeviantArt group page to extract the group's Eclispe ID from two
    possible places on the page.

    Args:
        group_name (string): DeviantArt group name.

    Returns:
        string: Eclipse group ID.
    """
    group_url = f"https://www.deviantart.com/{group_name}"

    start_time = time.time()
    page = requests.get(group_url)
    sleep_delay(start_time)

    soup = BeautifulSoup(page.text, 'html.parser')
    gmi = soup.find("div", {"name":"gmi-GBadge"})
    if gmi is not None:
        return gmi["gmi-owner"]
    gmi = soup.find("div", {"name":"gmi-Gruser"})
    if gmi is not None:
        return gmi["gmi-id"]
    print("ERROR")
    return None


def sleep_without_freeze(delay):
    """Pauses for a provided delay period without causing the script to freeze.

    Args:
        delay (int): Time in seconds to pause.
    """
    start = time.time()
    curr_seconds = int(start)
    curr_time = time.time()
    while curr_time < (start + delay):
        if int(curr_time) > curr_seconds:
            print('.', end='')
            curr_seconds = int(curr_time)
        curr_time = time.time()
    print()


def sleep_delay(start):
    """Pause the program for 15 times the duration of any call made to DeviantArt.

    Args:
        start (float): Unix timestamp representing the start time.
    """
    # wait 10x longer than it took them to respond
    response_delay = int(15 * (time.time() - start))
    print(f"                                 Sleeping {response_delay} seconds")
    sleep_without_freeze(response_delay)
