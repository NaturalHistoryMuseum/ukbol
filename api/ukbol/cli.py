import click
from flask.cli import FlaskGroup

from ukbol.app import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """
    CLI for UKBoL.

    This is extended off of the Flask CLI, so you can run flask commands through here
    too.
    """
    pass
