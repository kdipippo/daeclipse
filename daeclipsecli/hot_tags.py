"""Command to return top tags on the hottest deviations."""

import collections
import os

import cli_ui
import deviantart
import dotenv
import typer
from progress.bar import Bar

import daeclipse


def hot_tags(
    tag_count: int = typer.Option(  # noqa: B008, WPS404
        10,  # noqa: WPS425
        help='Number of top tags to return.',
    ),
    hot_count: int = typer.Option(  # noqa: B008, WPS404
        100,  # noqa: WPS425
        help='Number of hot deviations to process.',
    ),
):
    """Return top tags on the hottest deviations.

    Args:
        tag_count (int): --tag-count for number of tag results.
        hot_count (int): --hot-count for number of hot deviations to process.
    """
    eclipse = daeclipse.Eclipse()  # Internal Eclipse API wrapper.

    hottest_deviations = initialize_deviantart().browse(  # Public API wrapper.
        endpoint='popular',  # Popular also returns hottest.
        limit=hot_count,
    ).get('results')
    tags = []
    progressbar = Bar(
        'Parsing {0} hottest deviations'.format(hot_count),
        max=hot_count,
    )
    for deviation in hottest_deviations:
        progressbar.next()
        tags.extend(eclipse.get_deviation_tags(deviation.url))
    tags = collections.Counter(tags).most_common(tag_count)

    cli_ui.info()
    cli_ui.info_table(
        [
            [(cli_ui.bold, tag[0]), (cli_ui.green, tag[1])] for tag in tags
        ],
        headers=['tag', 'count'],
    )


def initialize_deviantart():
    """Initialize public API DeviantArt client. Collect creds if no .env found.

    Returns:
        deviantart.Api: deviantart.Api class instance.
    """
    dotenv_file = dotenv.find_dotenv()
    if dotenv_file == '':
        cli_ui.error('.env file not found. Creating and populating one now.')
        dotenv_file = '.env'
        client_id = None
        client_secret = None
    else:
        dotenv.load_dotenv(dotenv_file)
        client_id = os.getenv('deviantart_client_id')
        client_secret = os.getenv('deviantart_client_secret')

    if client_id is None or client_secret is None:
        cli_ui.info_1(
            'Obtain public API credentials at',
            cli_ui.underline,
            cli_ui.bold,
            'https://www.deviantart.com/developers/apps',
            cli_ui.reset,
        )

    if client_id is None:
        cli_ui.error('Missing deviantart_client_id')
        client_id = cli_ui.ask_password('Enter your dA client ID:')
        dotenv.set_key(dotenv_file, 'deviantart_client_id', client_id)

    if client_secret is None:
        cli_ui.error('Missing deviantart_client_secret')
        client_secret = cli_ui.ask_password('Enter your dA client secret:')
        dotenv.set_key(dotenv_file, 'deviantart_client_secret', client_secret)
    return deviantart.Api(client_id, client_secret)
