import click

from flask.cli import FlaskGroup
from flask import current_app
from resources.fixtures import create

from alayatodo import init_db, create_app

@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the Wiki application."""

@cli.command("initdb")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

@cli.command("fixtures")
def fixtures():
    """Create fixtures for development."""
    create()
    click.echo("Fixtures created.")

if __name__ == '__main__':
    cli()
