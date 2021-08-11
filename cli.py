"""Main file for DeviantArt Eclipse CLI."""

import typer

import daeclipsecli

app = typer.Typer(help='DeviantArt Eclipse CLI')

app.command()(daeclipsecli.add_art_to_groups)
app.command()(daeclipsecli.hot_tags)
app.command()(daeclipsecli.post_status)
app.command()(daeclipsecli.show_tags)
app.command()(daeclipsecli.spammer)
app.command()(daeclipsecli.user_comments)


if __name__ == '__main__':
    app()
