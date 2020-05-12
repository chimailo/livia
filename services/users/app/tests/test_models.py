from app.models import User


def test_encode_token(token):
    """ Token serializer encodes a JWT correctly. """
    assert token.decode().count('.') == 2


def test_decode_token(token):
    """ Token decoder decodes a JWT correctly. """
    payload = User.decode_auth_token(token.decode())
    user = User.find_by_id(payload.get('id'))
    assert user.email == 'admin@test.host'


def test_decode_token_tampered(token):
    """ Token decoder returns None when it's been tampered with. """
    id = User.decode_auth_token(f'{token.decode()}1337')
    assert isinstance(id, User) is False
