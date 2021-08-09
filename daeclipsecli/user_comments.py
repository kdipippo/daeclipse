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
        49,  # noqa: WPS425
        help='Total number of comments to return.',
    ),
    format: str = typer.Option(  # noqa: B008, WPS404
        'table',  # noqa: WPS425
        help='Output format, either list or table.',
    ),
):
    """Retrieve recent comments made by specified user.

    Args:
        username (str): DeviantArt username to query.
        offset (int): Offset to begin for paginated entry, defaults to 0.
        total (int): Total number of comments to return, defaults to max of 49.
        format (str): Output format, either list or table.
    """
    eclipse = daeclipse.Eclipse()
    comment_result = []
    has_more = True
    while len(comment_result) < total and has_more:
        user_comments_list = eclipse.get_user_comments(username, offset)
        offset = user_comments_list.next_offset
        has_more = user_comments_list.has_more
        comment_result.extend(user_comments_list.comments)
    comment_result = comment_result[:total]
    if format == 'list':
        for comm in comment_result:
            cli_ui.info('- {0}\n  {1}\n  {2}'.format(
                comm.get_url(),
                comm.comment.posted,
                comm.get_text(),
            ))
        return
    cli_ui.info(
        tabulate.tabulate(
            [
                [
                    comm.get_url(),
                    comm.comment.posted,
                    comm.get_text(),
                ] for comm in comment_result
            ],
            headers=['URL', 'Posted', 'Comment'],
            tablefmt='grid',
        ),
    )
