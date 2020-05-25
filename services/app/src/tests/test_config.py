import os
import unittest

from flask import current_app
from flask_testing import TestCase

from src import create_app


app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('src.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        """Test create_app with development config."""
        self.assertTrue(app.config['SECRET_KEY'] == 'top_secret')
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_DEV_URL')
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('src.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'top_secret')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_TEST_URL')
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('src.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['SECRET_KEY'] is not None)
        self.assertFalse(app.config['TESTING'])
        self.assertFalse(app.config['DEBUG'])

# def test_development_config(client):
#     """Test create_app with development config."""
#     app = create_app()
#     assert current_app is not None
#     assert app.config["SECRET_KEY"] == "secret_key"
#     assert app.config["SQLALCHEMY_DATABASE_URI"] == \
#         os.environ.get("DATABASE_DEV_URL")


# def test_testing_config(client):
#     """Test create_app with Test config."""
#     app = create_app(config=TestingConfig)
#     assert app.config["TESTING"] is True
#     assert app.config["SECRET_KEY"] == "secret_key"
#     assert app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] is False
#     assert app.config["SQLALCHEMY_DATABASE_URI"] == \
#         os.environ.get("DATABASE_TEST_URL")


# def test_production_config(client):
#     """Test create_app with development config."""
#     app = create_app(config=ProductionConfig)
#     assert app.config["SECRET_KEY"] is not None
#     assert app.config["TESTING"] is False
#     assert app.config["DEBUG"] is False
