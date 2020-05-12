import pytest

from app import create_app, db as _db
from app.config import TestingConfig
from app.models import User


@pytest.fixture(scope="session")
def app():
    """
    Create and configure a new app instance for each test.

    :returns -- object: Flask app
    """
    # create the app with test config.
    app = create_app(config=TestingConfig)

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(scope="function")
def client(app):
    """
    Setup an app client, this gets executed for each client.

    :arguments: app {object} -- Pytext fixture
    :return: Flask app client
    """
    return app.test_client()


@pytest.fixture(scope='session')
def db(app):
    """
    Setup our database, this only gets executed once per session.

    :param app: Pytest fixture
    :return: SQLAlchemy database session
    """
    _db.drop_all()
    _db.create_all()

    params = {
        'username': 'admin',
        'email': 'admin@test.host',
        'password': 'password',
    }

    admin = User(**params)

    _db.session.add(admin)
    _db.session.commit()

    return _db


@pytest.yield_fixture(scope='function')
def session(db):
    """
    Allow very fast tests by using rollbacks and nested sessions.
    :param db: Pytest fixture
    :return: None
    """
    db.session.begin_nested()
    yield db.session
    db.session.rollback()

    return db


@pytest.fixture(scope='function')
def users(db):
    """
    Create user fixtures. They reset per test.

    :param db: Pytest fixture
    :return: SQLAlchemy database session
    """
    db.session.query(User).delete()

    users = [
        {
            'username': 'admin',
            'email': 'admin@test.host',
            'password': 'password',
            'is_admin': True,
        },
        {
            'username': 'user1',
            'email': 'user1@test.host',
            'password': 'password',
        },
        {
            'username': 'disbled',
            'email': 'disabled@test.host',
            'password': 'password',
            'is_active': False,
        }
    ]

    for user in users:
        db.session.add(User(**user))

    db.session.commit()

    return db


@pytest.fixture(scope='module')
def token(db):
    """
    Serialize a JWT token.

    :param db: Pytest fixture
    :return: JWT token
    """
    user = User.find_by_identity('admin@test.host')
    return user.encode_auth_token(user.id)
