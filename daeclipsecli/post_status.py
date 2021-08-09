"""Command to post a DeviantArt status."""

import cli_ui

import daeclipse


def post_status():
    """Post a DeviantArt status."""
    eclipse = daeclipse.Eclipse()
    cli_ui.info_1('Deviation URL is required for CSRF token authentication.')
    deviation_url = cli_ui.ask_string('Paste deviation URL: ')
    status_content = cli_ui.ask_string('Enter HTML-formatted status text: ')

    try:
        status_result = eclipse.post_status(deviation_url, status_content)
    except RuntimeError as status_error:
        cli_ui.error(str(status_error))
    cli_ui.info(status_result)
