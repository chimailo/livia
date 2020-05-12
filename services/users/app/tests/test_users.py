import json

from app.models import User


def test_users(client):
    """
    Ensure the '/users/ping' route behaves correctly.

    GIVEN a Flask application
    WHEN the ping() route is requested (GET)
    THEN check the response is valid
    """
    response = client.get('/api/users/ping')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert "Users route" in data['message']


def test_get_user(client, users):
    """
    GIVEN a Flask application
    WHEN the get_user(id) route is requested (GET)
    THEN ensure the response is valid.
    """
    user = User.find_by_identity('admin@test.host')
    response = client.get(f'/api/users/{user.id}')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data.get('email') == 'admin@test.host'


def test_get_user_invalid_id(client, users):
    """
    GIVEN a Flask application
    WHEN the get_user(id) route is requested (GET) with an invalid id
    THEN ensure that the response is an error.
    """
    response = client.get('/api/users/66853')
    data = json.loads(response.data.decode())
    assert response.status_code == 404
    assert 'User not found' in data.get('message')
    assert 'Not Found' in data.get('error')


def test_all_users(client, users):
    """
    GIVEN a Flask application
    WHEN the get_users(page) route is requested (GET) with no param
    THEN ensure that the response is valid.
    """
    response = client.get('/api/users')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert len(data.get('items')) == 2


def test_all_users_with_pagination_first_page(client, users):
    """
    GIVEN a Flask application
    WHEN the get_users(page) route is requested (GET) with no page=1
    THEN ensure that the response is valid.
    """
    response = client.get('/api/users/page/1')
    data = json.loads(response.data.decode())
    print(data)
    assert response.status_code == 200
    assert len(data.get('items')) <= 2
    assert data.get('next_url') == '/api/users/page/2'
    assert data.get('prev_url') is None


def test_all_users_with_pagination_last_page(client, users):
    """
    GIVEN a Flask application
    WHEN the get_users(page) route is requested (GET) with no page=2
    THEN ensure that the response is valid.
    """
    response = client.get('/api/users/page/2')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert len(data.get('items')) <= 2
    assert data.get('prev_url') == '/api/users/page/1'
    assert data.get('next_url') is None


def test_add_user_no_data(client):
    """
    GIVEN a Flask application
    WHEN the add_user() route is requested (POST) with no data
    THEN ensure that the response is an error.
    """
    response = client.post('/api/users', data=json.dumps({}),
                        content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'No input data provided' in data.get('message')


def test_add_user_invalid_data(client):
    """
    GIVEN a Flask application
    WHEN the add_user() route is requested (POST) with invalid data
    THEN ensure that the response is an error.
    """
    response = client.post('/api/users', data=json.dumps({
        'username': 'test',
        'email': 'invalid@test.com'}),
        content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 422
    assert data.get('message') is not None


def test_add_user_duplicate_email(client):
    """
    GIVEN a Flask application
    WHEN the add_user() route is requested (POST) with duplicate email
    THEN ensure that the response is an error.
    """
    response = client.post('/api/users', data=json.dumps({
        'username': 'test',
        'email': 'user1@test.host',
        'password': 'password'}),
        content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'user already exists.' in data.get('message')


def test_add_user_duplicate_username(client):
    """
    GIVEN a Flask application
    WHEN the add_user() route is requested (POST) with duplicate username
    THEN ensure that the response is an error.
    """
    response = client.post('/api/users', data=json.dumps({
        'username': 'user1',
        'email': 'user@test.host',
        'password': 'password'}),
        content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'user already exists.' in data.get('message')


def test_add_user(client):
    """
    GIVEN a Flask application
    WHEN the add_user() route is requested (POST)
    THEN ensure that the response is valid.
    """
    response = client.post('/api/users', data=json.dumps({
        'username': 'user',
        'email': 'user@test.host',
        'password': 'password'}),
        content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert 'added new user' in data.get('message')
    assert response.headers['Location'] is not None


def test_update_user_duplicate_username(client, users):
    """
    GIVEN a Flask application
    WHEN the update_user() route is requested (PUT) with duplicate username
    THEN ensure that the response is an error.
    """
    user = User.find_by_identity('user1@test.host')
    response = client.put(f'/api/users/{user.id}', data=json.dumps({
        'firstname': 'user1',
        'username': 'admin',
        'email': 'user1@test.host',
        'password': 'password'}),
        content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'username already exists.' in data.get('message')


def test_update_user_no_data(client, users):
    """
    GIVEN a Flask application
    WHEN the update_user() route is requested (PUT) with no data
    THEN ensure that the response is an error.
    """
    user = User.find_by_identity('admin@test.host')
    response = client.put(f'/api/users/{user.id}', data=json.dumps({}),
                            content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'No input data provided' in data.get('message')


def test_update_user_invalid_data(client, users):
    """
    GIVEN a Flask application
    WHEN the update_user() route is requested (PUT) with invalid data
    THEN ensure that the response is an error.
    """
    response = client.put('/api/users/2', data=json.dumps({
        'firstname': 'test1',
        'username': 'w.',
        'bio': 'test user',
        'email': 'user1@test.host',
        'password': 'password'}),
        content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 422
    assert data.get('message') is not None


def test_update_user(client, users):
    """
    GIVEN a Flask application
    WHEN the update_user() route is requested (PUT)
    THEN ensure that the response is valid.
    """
    user = User.find_by_identity('user1@test.host')
    response = client.put(f'/api/users/{user.id}', data=json.dumps({
        'lastname': 'user1',
        'bio': 'test user',
        'is_admin': True,
        'email': 'user1@test.host',
        'password': 'password'}),
        content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 'updated user' in data.get('message')


def test_delete_user(client, users):
    """
    GIVEN a Flask application
    WHEN the delete_user() route is requested (DELETE)
    THEN ensure that the response is valid.
    """
    user = User.find_by_identity('disabled@test.host')
    response = client.delete(f'/api/users/{user.id}')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 'deleted user' in data.get('message')


def test_delete_user_invalid_id(client, users):
    """
    GIVEN a Flask application
    WHEN the delete_user() route is requested (DELETE) with invalid id
    THEN ensure that the response is valid.
    """
    response = client.delete('/api/users/333')
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'User does not exist.' in data.get('message')
