from pathlib import Path

import click
from flask.cli import FlaskGroup

from ukbol.app import create_app
from ukbol.data.bold import rebuild_bold_tables
from ukbol.data.uksi import rebuild_uksi_tables
from ukbol.utils import create_all_tables


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """
    CLI for UKBoL.

    This is extended off of the Flask CLI, so you can run flask commands through here
    too.
    """
    pass


@cli.command("rebuild-uksi")
@click.argument("uksi_dwca", type=click.Path(exists=True, dir_okay=False))
def rebuild_uksi(uksi_dwca: Path):
    # todo: make migrations and remove
    create_all_tables()
    rebuild_uksi_tables(uksi_dwca)


@cli.command("rebuild-bold")
@click.argument("bold_snapshot", type=click.Path(exists=True, dir_okay=False))
def rebuild_bold(bold_snapshot: Path):
    # todo: make migrations and remove
    create_all_tables()
    rebuild_bold_tables(bold_snapshot)


if __name__ == "__main__":
    cli()
