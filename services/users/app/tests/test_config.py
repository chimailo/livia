import os

from flask import current_app

from app import create_app
from app.config import TestingConfig, ProductionConfig


def test_development_config(client):
    """Test create_app with development config."""
    app = create_app()
    assert current_app is not None
    assert app.config["SECRET_KEY"] == "secret_key"
    assert app.config["SQLALCHEMY_DATABASE_URI"] == \
        os.environ.get("DATABASE_URL")


def test_testing_config(client):
    """Test create_app with Test config."""
    app = create_app(config=TestingConfig)
    assert app.config["TESTING"] is True
    assert app.config["SECRET_KEY"] == "secret_key"


def test_production_config(client):
    """Test create_app with development config."""
    app = create_app(config=ProductionConfig)
    assert app.config["SECRET_KEY"] == "secret_key"
    assert app.config["TESTING"] is False
    assert app.config["DEBUG"] is False
