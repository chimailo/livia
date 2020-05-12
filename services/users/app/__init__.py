import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# set up extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

app_settings = os.getenv("APP_SETTINGS")


def create_app(config=app_settings):
    """
    Create a Flask application using the app factory pattern.

    :return - object: Flask app
    """
    # Instantiate app
    app = Flask(__name__)

    # Set configuration
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    @app.route("/ping")
    def ping():
        return {"message": "Ping!"}

    # Register Blueprint
    from app.routes.users import users
    app.register_blueprint(users)

    from app.routes.auth import auth
    app.register_blueprint(auth)

    from app.errors import errors
    app.register_blueprint(errors)

    @app.shell_context_processor
    def ctx():
        """shell context for flask cli """
        return {"app": app, "db": "db"}

    return app


from app.models import User
