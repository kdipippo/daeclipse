"""Command to assist with reporting DeviantArt users for spam."""

from itertools import combinations

import cli_ui

import daeclipse


def spammer(
    username: str,
):
    """Return information and output for spam report helpdesk ticket creation.

    Args:
        username (str): DeviantArt username to query.
    """
    eclipse = daeclipse.Eclipse()
    comment_result = []
    has_more = True
    while has_more:
        user_comments_list = eclipse.get_user_comments(username)
        has_more = user_comments_list.has_more
        comment_result.extend(user_comments_list.comments)

    cli_ui.info(cli_ui.bold, spammer_cmd_header(username), cli_ui.reset)
    cli_ui.info(
        spammer_cmd_body(
            username,
            comment_result,
        ),
    )


class LCSTracker(object):
    """Helper class for Longest Common Substring grid and functionality."""

    def __init__(self, string_a, string_b):
        """Initialize Longest Common Substring tracker with placeholder values.

        Args:
            string_a (str): First string.
            string_b (str): Second string.
        """
        self.len_a = len(string_a)
        self.len_b = len(string_b)

        # Track length of longest common substring.
        self.max_length = 0

        # Track index of cell containing max value.
        self.max_row = 0
        self.max_col = 0

        # Init grid to 2D array of 0s to store longest common suffix lens.
        self.grid = []
        for _rows in range(self.len_a + 1):  # noqa: WPS122
            self.grid.append([0 for _cols in range(self.len_b + 1)])

    def update_max(self, new_max_length, index_a, index_b):
        """Update current known longest common substring length and coords.

        Args:
            new_max_length ([type]): New length of longest common substring.
            index_a ([type]): X coordinate for start of substring.
            index_b ([type]): Y coordinate for start of substring.
        """
        self.max_length = new_max_length
        self.max_row = index_a
        self.max_col = index_b

    def traverse_upleft_diagonally(self):
        """Update current cell coordinates to move diagonally up and left."""
        self.max_row -= 1
        self.max_col -= 1

    def get_cell(self, index_a=None, index_b=None):
        """Return cell value of grid at coordinate.

        Args:
            index_a ([type]): X coordinate in grid.
            index_b ([type]): Y coordinate in grid.

        Returns:
            int: Value of cell in grid, the tracked length of substring.
        """
        return self.grid[index_a][index_b]

    def update_cell(self, index_a, index_b, new_length):
        """Update cell at coordinate and check if new value beats current max.

        Args:
            index_a ([type]): X coordinate in grid.
            index_b ([type]): Y coordinate in grid.
            new_length ([type]): New value to store in grid at coordinate.
        """
        self.grid[index_a][index_b] = new_length

        if new_length != 0 and new_length > self.max_length:
            self.update_max(new_length, index_a, index_b)

    def get_curr_cell(self):
        """Return current stored value of stored max row and col coordinates.

        Returns:
            int: Value at stored max row and col coordinates in grid.
        """
        return self.grid[self.max_row][self.max_col]

    def assemble_lcs(self, string_a):
        """Return longest common substring based on results of generated grid.

        Args:
            string_a (str): First string, used for extracting substring.

        Returns:
            str: Longest common substring result.
        """
        # No common substring exists.
        if self.max_length == 0:
            return ''

        # Allocate space for the longest common substring.
        result_lcs = ['0' for _ in range(self.max_length)]

        # Traverse up diagonally, form (row, col) cells.
        while self.get_curr_cell() != 0:
            self.max_length -= 1
            result_lcs[self.max_length] = string_a[self.max_row - 1]
            self.traverse_upleft_diagonally()

        return ''.join(result_lcs)


def get_longest_substring(string_a: str, string_b: str):
    """Return longest common substring of two strings.

    Args:
        string_a (str): First string.
        string_b (str): Second string.

    Returns:
        str: Longest substring between string_a and string_b, "" if none.
    """
    lcst = LCSTracker(string_a, string_b)

    # Build LCSTracker grid from bottom up.
    for index_a in range(lcst.len_a + 1):
        for index_b in range(lcst.len_b + 1):
            if strings_match_at_indices(string_a, index_a, string_b, index_b):
                lcst.update_cell(
                    index_a,
                    index_b,
                    lcst.get_cell(index_a - 1, index_b - 1) + 1,
                )
            else:
                lcst.update_cell(index_a, index_b, 0)
    return lcst.assemble_lcs(string_a)


def strings_match_at_indices(string_a, index_a, string_b, index_b):
    """Check if both strings match at given indices and indices aren't 0.

    Args:
        string_a (str): First string.
        index_a (int): Index of character in first string.
        string_b (str): Second string.
        index_b (int): Index of character in second string.

    Returns:
        boolean: If both strings match at given indices and indices aren't 0.
    """
    if index_a == 0:
        return False
    if index_b == 0:
        return False
    return string_a[index_a - 1] == string_b[index_b - 1]


def get_longest_substrings(full_strings):
    """Return a dict of top substrings with hits from a given list of strings.

    Args:
        full_strings (list[str]): List of strings to test against each other.

    Returns:
        dict: substrings with their respective frequencies in full_strings.
    """
    combos = list(combinations(full_strings, 2))

    all_substrings = {}
    for string_a, string_b in combos:
        substring = get_longest_substring(string_a, string_b)
        # Set entry to 2, matches with string_a and string_b, else + 1.
        all_substrings.update(
            {
                substring: all_substrings.get(substring, 1) + 1,
            },
        )
    return all_substrings


def get_spam_string(full_strings):
    """Return key with largest value from longest common substrings (LCS) dict.

    Args:
        full_strings (list[str]): List of strings to compare for LCS.

    Returns:
        str: Longest common substring.
    """
    exclude_flagged = [
        'Flagged as Spam',
        'Hidden by Owner',
        'Hidden by Commenter',
    ]
    spam_strings = list(get_longest_substrings(full_strings).keys())
    spam_strings.sort(key=len, reverse=True)
    for spam_string in spam_strings:
        if spam_string not in exclude_flagged:
            return spam_string


def spammer_cmd_header(username):
    """Return formatted text for spammer command header.

    Args:
        username (str): DeviantArt username.

    Returns:
        str: Formatted text for spammer command header.
    """
    return '\n'.join([
        'REPORT LINK: https://contact.deviantartsupport.com/en?subOptionId=How-do-I-report-Spam?78094',  # noqa: E501
        '',
        '',
        'Report Spammer: {username}',
    ]).format(
        username=username,
    )


def spammer_cmd_body(username, comment_result):
    """Return formatted text for spammer command body.

    Args:
        username (str): DeviantArt username.
        comment_result (list[UserComment]): List of UserComment objects.

    Returns:
        str: Formatted text for spammer command body.
    """
    comments = [comm.get_text() for comm in comment_result]
    spam_string = get_spam_string(comments)

    urls = []
    for comm in comment_result:
        direct_match_flag = ''
        if spam_string in comm.get_text():
            direct_match_flag = '** '

        urls.append(
            '- {0}{1}'.format(
                direct_match_flag,
                comm.get_url(),
            ),
        )

    return '\n'.join([
        '{username} frequently spams "{top_spam_string}"',
        '',
        'All recent comments: https://www.deviantart.com/{username}/about#my_comments',  # noqa: E501
        'URLs marked with ** have exact matches to the spam text above.',
        '',
        '{comment_urls}',
    ]).format(
        username=username,
        top_spam_string=spam_string,
        comment_urls='\n'.join(urls),
    )
