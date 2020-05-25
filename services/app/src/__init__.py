import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


# set up extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()


def create_app(script_info=None):
    """
    Create a Flask application using the app factory pattern.

    :return - object: Flask app
    """
    # Instantiate app
    app = Flask(__name__)

    # Set configuration
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Register Blueprint
    from src.blueprints.auth.routes import auth
    app.register_blueprint(auth)

    from src.blueprints.profiles.routes import profile
    app.register_blueprint(profile)

    from src.blueprints.errors import errors
    app.register_blueprint(errors)

    @app.shell_context_processor
    def ctx():
        """shell context for flask cli """
        return {"app": app, "db": db}

    return app


from src.blueprints.auth.models import User
from src.blueprints.profiles.models import Profile
from src.blueprints.teams.models import Team
