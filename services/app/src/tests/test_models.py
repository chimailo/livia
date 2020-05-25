import unittest

from src.tests.base import BaseTestCase
from src.tests.utils import add_user, create_token
from src.blueprints.auth.models import User

from flask import current_app


# auth
#############
class TestAuthModel(BaseTestCase):
    def test_password_hashing(self):
        user = add_user(firstname='test', lastname='user4',
                        email='testuser4@test.com')
        self.assertFalse(user.check_password('secret'))
        self.assertTrue(user.check_password('password'))

    def test_encode_token(self):
        """ Token serializer encodes a JWT correctly. """
        token = create_token()
        self.assertEqual(token.count('.'), 2)

    def test_decode_token(self):
        """ Token decoder decodes a JWT correctly. """
        token = create_token()
        payload = User.decode_auth_token(token)
        user = User.find_by_id(payload.get('id'))
        self.assertTrue(isinstance(user, User)) 
        self.assertEqual(user.email, 'testuser3@test.com')

    def test_decode_token_invalid(self):
        """ Token decoder returns 'Invalid token' when
        it's been tampered with."""
        token = create_token()
        payload = User.decode_auth_token(f'{token}1337')
        self.assertFalse(isinstance(payload, User))
        self.assertIn('Invalid token', payload)

    def test_decode_token_expired(self):
        """ Token decoder returns None when it's been tampered with. """
        current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1
        token = create_token()
        payload = User.decode_auth_token(token)
        self.assertFalse(isinstance(payload, User)) 
        self.assertIn('Signature expired', payload)


# profile
#############
class TestProfileModel(BaseTestCase):
    def test_avatar(self):
        user = add_user(firstname='test', lastname='user4',
                        email='testuser4@test.com')
        self.assertEqual(user.profile.avatar, ('https://www.gravatar.com/avatar/'
                        'd9e37dcab16de69bf70af29f379656c6?s=128&d=mm&r=pg'))
