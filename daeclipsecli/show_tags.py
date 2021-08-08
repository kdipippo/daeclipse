"""Command to return list of tags for given deviation."""

import cli_ui
import typer

import daeclipse


def show_tags(
    deviation_url: str = typer.Option(  # noqa: B008, WPS404
        '',  # noqa: WPS425
        help='Deviation URL to retrieve tags from.',
    ),
):
    """Return list of tags for given deviation.

    Args:
        deviation_url (str): --deviation_url to specify deviation URL.
    """
    eclipse = daeclipse.Eclipse()
    if not deviation_url:
        deviation_url = cli_ui.ask_string('Paste deviation URL: ')
    tags = eclipse.get_deviation_tags(deviation_url)
    cli_ui.info_1(tags)
