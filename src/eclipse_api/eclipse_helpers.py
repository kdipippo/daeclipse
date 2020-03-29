#!/usr/bin/env python
"""Helper file containing HTML parsing functions for using Eclipse API methods."""

import requests
import time
from bs4 import BeautifulSoup

def get_csrf(deviation_url, cookies):
    """Parses the HTML of the deviation to get the csrf token in the page. It's stored as the
    value of a hidden input with name 'validate_token'.

    Arguments:
        deviation_url {string} -- deviation URL, i.e. https://da.com/art/Art-12345.
        http.cookiejar.CookieJar object -- .deviantart.com Cookie Jar.

    Returns:
        string -- CSRF validation token.
    """
    start_time = time.time()
    print("requests.get for get_csrf")
    page = requests.get(deviation_url, cookies=cookies)
    sleep_delay(start_time)

    soup = BeautifulSoup(page.text, 'html.parser')
    return soup.find("input", {"name":"validate_token"})["value"]

def get_group_id(group_name):
    """Parses the HTML of a DeviantArt group page to extract the group's Eclispe ID from two
    possible places on the page.

    Arguments:
        group_name {string} -- DeviantArt group name.

    Returns:
        string -- Eclipse group ID.
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

def custom_sleep(delay):
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

    Arguments:
        start {float} -- Unix timestamp representing the start time.
    """
    # wait 10x longer than it took them to respond
    response_delay = int(15 * (time.time() - start))
    print(f"                                 Sleeping {response_delay} seconds")
    custom_sleep(response_delay)