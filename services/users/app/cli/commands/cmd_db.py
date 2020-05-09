import click

from app import create_app, db


# Create an app context for the database connection.
app = create_app()
db.app = app


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass


@click.command()
def init():
    """
    Initialize the database.

    :return: None
    """
    db.drop_all()
    db.create_all()
    db.session.commit()
    click.echo("Successfully (re)created all databases...")

    return None


cli.add_command(init)
