import json
import time

from app.models import User


def test_auth(client):
    """
    GIVEN a Flask application
    WHEN the ping() route is requested (POST)
    THEN ensure the response is valid
    """
    response = client.get('/api/auth/ping')
    data = json.loads(response.data.decode())
    assert response.status_code == 200


def test_check_email_does_not_exist(client, users):
    """
    GIVEN a Flask application
    WHEN the ping() route is requested (POST)
    THEN ensure the response is valid
    """
    response = client.post(
        '/api/auth/check-email',
        data=json.dumps({'email': 'user@test.host'}),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data.get('res') is True


def test_check_email_do_exist(client, users):
    """
    GIVEN a Flask application
    WHEN the check_email() route is requested (POST)
    THEN ensure the response is valid
    """
    response = client.post(
        '/api/auth/check-email',
        data=json.dumps({'email': 'user1@test.host'}),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data.get('res') is not True


def test_check_username_does_not_exist(client, users):
    """
    GIVEN a Flask application
    WHEN the check_username() route is requested (POST)
    THEN ensure the response is valid
    """
    response = client.post(
        '/api/auth/check-username',
        data=json.dumps({'username': 'user'}),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data.get('res') is True


def test_check_username_do_exist(client, users):
    """
    GIVEN a Flask application
    WHEN the check_username() route is requested (POST)
    THEN ensure the response is valid
    """
    response = client.post(
        '/api/auth/check-username',
        data=json.dumps({'username': 'user1'}),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data.get('res') is not True


def test_register_user_no_data(client):
    """
    GIVEN a Flask application
    WHEN the register_user() route is requested (POST) with no data
    THEN ensure that the response is an error.
    """
    response = client.post(
        '/api/auth/register',
        data=json.dumps({}),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'No input data provided' in data.get('message')


def test_register_user_invalid_data(client):
    """
    GIVEN a Flask application
    WHEN the register_user() route is requested (POST) with invalid data
    THEN ensure that the response is an error.
    """
    response = client.post(
        '/api/auth/register',
        data=json.dumps({
            'username': 'test',
            'email': 'invalidtest.com',
            'password': 'pass'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 422
    assert data.get('message') is not None


def test_register_user_duplicate_username(client, users):
    """
    GIVEN a Flask application
    WHEN the register_user() route is requested (POST) with duplicate username
    THEN ensure that the response is an error.
    """
    response = client.post(
        '/api/auth/register',
        data=json.dumps({
            'username': 'disabled',
            'email': 'user1@test.host',
            'password': 'password'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'user already exists.' in data.get('message')


def test_register_user(client, users):
    """
    GIVEN a Flask application
    WHEN the register_user() route is requested (POST)
    THEN ensure that the response is valid.
    """
    response = client.post(
        '/api/auth/register',
        data=json.dumps({
            'email': 'user2@test.host',
            'password': 'password'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert response.headers['Location'] is not None
    assert 'Sign up was successful' in data.get('message')
    assert data.get('token') is not None


def test_registered_user_login(client, users):
    """
    GIVEN a Flask application
    WHEN a registered user requests the login_user() route (POST)
    THEN ensure that the response is valid.
    """
    user = User.find_by_identity('admin@test.host')
    old_sign_in_count = user.sign_in_count

    response = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'admin@test.host',
            'password': 'password'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())

    new_sign_in_count = user.sign_in_count

    assert response.status_code == 200
    assert data.get('token') is not None
    assert (old_sign_in_count + 1) == new_sign_in_count


def test_login_user_incorrect_password(client, users):
    """
    GIVEN a Flask application
    WHEN a user requests the login_user() route (POST)
        with an incorrect password
    THEN ensure that the response is valid.
    """
    response = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'user1@test.host',
            'password': 'passwords'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 401
    assert 'Incorrect email or password' in data.get('message')
    assert data.get('token') is None


def test_not_registered_user_login(client, users):
    """
    GIVEN a Flask application
    WHEN an unregistered user requests the login_user() route (POST)
    THEN ensure that the response is valid.
    """
    response = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'user@test.host',
            'password': 'password'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'Invalid payload' in data.get('message')
    assert data.get('token') is None


def test_logout_user(client, token):
    """
    GIVEN a Flask application
    WHEN a user requests the logout_user() route (GET)
    THEN ensure that the response is an error.
    """
    response = client.get(
        '/api/auth/logout',
        headers={'Authorization': f'Bearer {token.decode()}'}
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 'logged out' in data.get('message')


def test_get_user(client, token):
    """
    GIVEN a Flask application
    WHEN a user requests the get_user() route (GET)
    THEN ensure that the response is valid.
    """
    response = client.get(
        '/api/auth/user',
        headers={'Authorization': f'Bearer {token.decode()}'}
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data is not None


def test_logout_expired_token(client, token):
    """
    GIVEN a Flask application
    WHEN a user requests the logout_user() route (GET)
    THEN ensure that the response is an error.
    """
    time.sleep(4)
    response = client.get(
        '/api/auth/logout',
        headers={'Authorization': f'Bearer {token.decode()}'}
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 401
    assert 'Signature expired' in data.get('message')


def test_logout_invalid_token(client, token):
    """
    GIVEN a Flask application
    WHEN a user requests the logout_user() route (GET) with invalid token
    THEN ensure that the response is an error.
    """
    response = client.get(
        '/api/auth/logout',
        headers={'Authorization': 'Bearer invalid'}
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 401
    assert 'Invalid token.' in data.get('message')


def test_get_user_invalid(client, token):
    """
    GIVEN a Flask application
    WHEN a user requests the get_user() route (GET) with an invalid token
    THEN ensure that the response is valid.
    """
    response = client.get(
        '/api/auth/user',
        headers={'Authorization': 'Bearer invalid'}
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 401
    assert 'Invalid token' in data.get('message')
