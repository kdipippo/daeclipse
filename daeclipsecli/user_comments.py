"""Command to retrieve recent comments made by specified user."""

import cli_ui
import tabulate
import typer

import daeclipse


def user_comments(
    username: str,
    offset: int = typer.Option(  # noqa: B008, WPS404
        0,  # noqa: WPS425
        help='Offset to begin for paginated entry.',
    ),
    total: int = typer.Option(  # noqa: B008, WPS404
        49,  # noqa: WPS425, WPS432
        help='Total number of comments to return.',
    ),
    output: str = typer.Option(  # noqa: B008, WPS404
        'table',  # noqa: WPS425
        help='Output format, either list or table.',
    ),
):
    """Retrieve recent comments made by specified user.

    Args:
        username (str): DeviantArt username to query.
        offset (int): Offset to begin for paginated entry, defaults to 0.
        total (int): Total number of comments to return, defaults to max of 49.
        output (str): Output format, either list or table.
    """
    # 49 is max num of recent comments Eclipse API allows with this endpoint.
    eclipse = daeclipse.Eclipse()
    comment_result = []
    has_more = True
    while len(comment_result) < total and has_more:
        user_comments_list = eclipse.get_user_comments(username, offset)
        offset = user_comments_list.next_offset
        has_more = user_comments_list.has_more
        comment_result.extend(user_comments_list.comments)
    comment_result = comment_result[:total]

    cli_ui.info(format_results(output, comment_result))


def format_results(output, comment_result):
    """Return formatted result based on provided format.

    Args:
        output (str): Output format, either list or table.
        comment_result (UserComment[]): List of user's comments.

    Returns:
        str: Formatted results.
    """
    if output == 'list':
        return format_results_list(comment_result)

    # Default to 'table' formatting.
    return format_results_table(comment_result)


def format_results_list(comment_result):
    """Return formatted results as a list.

    Args:
        comment_result (UserComment[]): List of user's comments.

    Returns:
        str: Formatted results as a list.
    """
    list_rows = []
    for comm in comment_result:
        list_rows.append(
            '- {0}\n  {1}\n  {2}'.format(
                comm.get_url(),
                comm.get_posted_date(),
                comm.get_text(),
            ),
        )
    return '\n'.join(list_rows)


def format_results_table(comment_result):
    """Return formatted results as a table.

    Args:
        comment_result (UserComment[]): List of user's comments.

    Returns:
        str: Formatted results as a table.
    """
    table_rows = []
    for comm in comment_result:
        table_rows.append([
            comm.get_url(),
            comm.get_posted_date(),
            comm.get_text(),
        ])
    return tabulate.tabulate(
        table_rows,
        headers=['URL', 'Posted', 'Comment'],
        tablefmt='grid',
    )
