"""Command to assist with reporting DeviantArt users for spam."""

import cli_ui
from itertools import combinations
import operator

import daeclipse


def spammer(
    username: str,
):
    """Return information and output for spam report helpdesk ticket creation.

    Args:
        username (str): DeviantArt username to query.
    """
    cli_ui.info_1(cli_ui.bold, 'REPORT LINK: https://contact.deviantartsupport.com/en?subOptionId=How-do-I-report-Spam?78094\n', cli_ui.reset)
    cli_ui.info(cli_ui.bold, "Report Spammer: {0}\n".format(username), cli_ui.reset)

    eclipse = daeclipse.Eclipse()
    comment_result = []
    has_more = True
    while has_more:
        user_comments_list = eclipse.get_user_comments(username)
        has_more = user_comments_list.has_more
        comment_result.extend(user_comments_list.comments)

    urls = []
    comments = []
    for comm in comment_result:
        comments.append(comm.get_text())
        urls.append('- {0}'.format(comm.get_url()))

    cli_ui.info('{0} frequently posts "{1}"'.format(username, get_spam_string(comments)))
    cli_ui.info()
    cli_ui.info('All recent comments: https://www.deviantart.com/{0}/about#my_comments\n'.format(username))
    cli_ui.info('\n'.join(urls))







def get_longest_substring(string_a: str, string_b: str):
    """Return longest common substring of two strings.

    Args:
        string_a (str): First string.
        string_b (str): Second string.

    Returns:
        str: Longest substring between string_a and string_b, "" if none.
    """
    len_a = len(string_a)
    len_b = len(string_b)

    # 2D array to store lengths of longest common suffixes.
    len_lcsuffixes = [
        [0 for i in range(len_b + 1)] for j in range(len_a + 1)
    ]

    length = 0  # Track length of longest common substring.
    row, col = 0, 0  # Track index of cell containing max value.

    # Build len_lcsuffixes[m+1][n+1] from bottom up.
    for i in range(len_a + 1):
        for j in range(len_b + 1):
            if i == 0 or j == 0:
                len_lcsuffixes[i][j] = 0
            elif string_a[i - 1] == string_b[j - 1]:
                len_lcsuffixes[i][j] = len_lcsuffixes[i - 1][j - 1] + 1
                if length < len_lcsuffixes[i][j]:
                    length = len_lcsuffixes[i][j]
                    row = i
                    col = j
            else:
                len_lcsuffixes[i][j] = 0

    if length == 0:
        # No common substring exists.
        return ""

    # Allocate space for the longest common substring.
    resultStr = ['0'] * length

    # Traverse up diagonally, form (row, col) cells..
    while len_lcsuffixes[row][col] != 0:
        length -= 1
        resultStr[length] = string_a[row - 1]

        # Move diagonally up to previous cell.
        row -= 1
        col -= 1

    # required longest common substring
    return ''.join(resultStr)


def get_longest_substrings(full_strings):
    """Return a dict of top substrings with hits from a given list of strings.

    Args:
        full_strings (str[]): List of strings to find patterning substrings.

    Returns:
        dict: substrings with their respective frequencies in full_strings.
    """
    combos = list(combinations(full_strings, 2))

    substrings = {}
    for string_a, string_b in combos:
        substring = get_longest_substring(string_a, string_b)
        if len(substring) <= 1:
            continue
        if substring in substrings:
            substrings[substring] += 1
        else:
            # The substring has 2 matches with string_a and string_b.
            substrings[substring] = 2
    return substrings

def get_spam_string(full_strings):
    spam_strings = get_longest_substrings(full_strings)
    return max(spam_strings.items(), key = operator.itemgetter(1))[0]
