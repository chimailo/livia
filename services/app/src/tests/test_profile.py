import json
import unittest

from src.tests.base import BaseTestCase
from src.tests.utils import create_token, add_user


class TestProfileBlueprint(BaseTestCase):
    def test_check_username_does_not_exist(self):
        token = create_token()
        response = self.client.post(
            '/api/profile/check-username',
            headers={'Authorization': f'Bearer {token}'},
            data=json.dumps({'username': 'user'}),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('res'))

    def test_check_username_do_exist(self):
        user = add_user(firstname='test', lastname='user6',
        username='testuser6', email='testuser6@test.com')
        token = create_token()
        response = self.client.post(
            '/api/profile/check-username',
            data=json.dumps({'username': 'testuser6'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'},
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(data.get('res'))

    def test_get_profile(self):
        token = create_token()
        response = self.client.get(
            '/api/profile',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('user') is not None)
        self.assertTrue(data.get('profile') is not None)

    def test_update_profile(self):
        token = create_token()
        response = self.client.put(
            '/api/profile',
            data=json.dumps({
                'firstname': 'user',
                'lastname': 'admin',
                'username': 'useradmin',
                'bio': 'I am the admin'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('updated your profile', data.get('message'))

    def test_update_profile_username_exists(self):
        add_user(firstname='test', lastname='user2',
        username='testuser2', email='testuser2@test.com')
        token = create_token()
        response = self.client.put(
            '/api/profile',
            headers={'Authorization': f'Bearer {token}'},
            data=json.dumps({
                'firstname': 'user',
                'lastname': 'test',
                'username': 'testuser2',
                'bio': 'I am the admin'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("already taken", data.get('message'))

    def test_update_profile_invalid_data(self):
        token = create_token()
        response = self.client.put(
            '/api/profile',
            headers={'Authorization': f'Bearer {token}'},
            data=json.dumps({
                'firstname': 'u',
                'bio': 'I am the admin'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data.get('error') is None)

    def test_delete_profile(self):
        token = create_token()
        response = self.client.delete(
            '/api/profile',
            headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 200)
