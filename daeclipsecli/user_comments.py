"""Command to retrieve recent comments made by specified user."""

import cli_ui
import typer

import daeclipse


def user_comments(
    username: str,
    offset: int = typer.Option(  # noqa: B008, WPS404
        0,  # noqa: WPS425
        help='Offset to begin for paginated entry.',
    ),
    total: int = typer.Option(  # noqa: B008, WPS404
        10,  # noqa: WPS425
        help='Total number of comments to return.',
    ),
):
    """Retrieve recent comments made by specified user.

    Args:
        username (str): DeviantArt username to query.
        offset (int): Offset to begin for paginated entry, defaults to 0.
        total (int): Total number of comments to return, defaults to 10.
    """
    eclipse = daeclipse.Eclipse()
    user_comments = []
    has_more = True
    while len(user_comments) < total or has_more:
        user_comments_list = eclipse.get_user_comments(username, offset)
        offset = user_comments_list.next_offset
        has_more = user_comments_list.has_more
        user_comments.extend(user_comments_list.comments)
    user_comments = user_comments[:total]
    cli_ui.info_table(
        [
            [(cli_ui.bold, user_comment.comment.comment_id), (cli_ui.green, user_comment.comment.text_content.excerpt)] for user_comment in user_comments
        ],
        headers=['ID', 'Comment'],
    )
