from src import app, db
from src.blueprints.auth.models import User
from src.blueprints.profiles.models import Profile


@app.shell_context_processor
def ctx():
    """shell context for flask cli """
    return {
        "app": app,
        "db": db,
        'User': User,
        'Profile': Profile
    }
