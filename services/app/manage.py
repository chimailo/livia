import os
import subprocess
import sys
import unittest

import click
from flask.cli import FlaskGroup

from src import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
@click.argument("path", default="app")
def cov(path):
    """
    Run a test coverage report.

    :param path: Test coverage path
    :return: Subprocess call result
    """
    cmd = "py.test --cov-report term-missing --cov {0}".format(path)
    return subprocess.call(cmd, shell=True)


@cli.command()
@click.option(
    "--skip-init/--no-skip-init",
    default=True,
    help="Skip __init__.py files?"
)
@click.argument("path", default="app")
def flake8(skip_init, path):
    """
    Run flake8 to analyze your code base.

    :param skip_init: Skip checking __init__.py files
    :param path: Test coverage path
    :return: Subprocess call result
    """
    flake8_flag_exclude = ""

    if skip_init:
        flake8_flag_exclude = " --exclude __init__.py"

    cmd = f"flake8 {path}{flake8_flag_exclude} --ignore E128 E402 f401"
    return subprocess.call(cmd, shell=True)


@cli.command()
@click.argument("path", default=os.path.join("src", "tests"))
def test(path):
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('src/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command()
def db_init():
    """Initialize the database."""
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Successfully (re)created all databases...")
    return None


if __name__ == '__main__':
    cli()
