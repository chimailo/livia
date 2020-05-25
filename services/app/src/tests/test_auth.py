import json
import unittest

from src.tests.base import BaseTestCase
from src.tests.utils import add_user, create_token


class TestAuthBlueprint(BaseTestCase):
    def test_check_email_does_not_exist(self):
        with self.client:
            response = self.client.post(
                '/api/auth/check-email',
                data=json.dumps({'email': 'testuser@test.host'}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data.get('res'))

    def test_check_email_do_exist(self):
        add_user(firstname='test', lastname='user1',
                email='testuser1@test.com')
        with self.client:
            response = self.client.post(
                '/api/auth/check-email',
                data=json.dumps({'email': 'testuser1@test.com'}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertFalse(data.get('res'))

    def test_register_user_no_data(self):
        with self.client:
            response = self.client.post(
                '/api/auth/register',
                data=json.dumps({}),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 400)

    def test_register_user_invalid_data(self):
        with self.client:
            response = self.client.post(
                '/api/auth/register',
                data=json.dumps({
                    'firstname': 'test',
                    'email': 'invalidtest.com',
                    'password': 'pass'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 422) 
            self.assertFalse(data.get('message') is None)

    def test_register_user(self):
        with self.client:
            response = self.client.post(
                '/api/auth/register',
                data=json.dumps({
                    'firstname': 'common',
                    'lastname': 'user',
                    'email': 'commonuser@test.host',
                    'password': 'password',
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertFalse(response.headers['Location'] is None)
            self.assertFalse(data.get('token') is None)

    def test_valid_user_login(self):
        user = add_user(firstname='test', lastname='user2',
                        email='testuser2@test.com')
        old_sign_in_count = user.sign_in_count

        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': 'testuser2@test.com',
                'password': 'password'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        new_sign_in_count = user.sign_in_count

        self.assertEqual(response.status_code, 200) 
        self.assertFalse(data.get('token') is None) 
        self.assertEqual((old_sign_in_count + 1), new_sign_in_count)

    def test_login_user_incorrect_password(self):
        add_user(firstname='test', lastname='user2',
                email='testuser2@test.com')
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': 'testuser2@test.com',
                'password': 'kkl'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertIn('Incorrect email or password', data.get('message'))
        self.assertTrue(data.get('token') is None)

    def test_invalid_user_login(self):
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': 'user@test.host',
                'password': 'password'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload', data.get('message'))
        self.assertTrue(data.get('token') is None)

    def test_logout_user(self):
        token = create_token()
        response = self.client.get(
            '/api/auth/logout',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('logged out', data.get('message'))

    def test_get_user(self):
        """
        GIVEN a Flask application
        WHEN a user requests the get_user() route (GET)
        THEN ensure that the response is valid.
        """
        token = create_token()
        response = self.client.get(
            '/api/auth/user',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(data.get('user') is None)
        self.assertFalse(data.get('profile') is None)
