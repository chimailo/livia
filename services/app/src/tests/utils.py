from src.blueprints.auth.models import User
from src.blueprints.profiles.models import Profile
# from src.blueprints.teams.models import Team


def add_user(firstname='', lastname='', username='', email='',
            is_admin=False, is_active=True):
    p = Profile(firstname=firstname, lastname=lastname)
    p.username = username or p.set_username()
    p.avatar = p.set_avatar(email)

    user = User(email=email, password='password', is_admin=is_admin,
                is_active=is_active, profile=p)
    user.save()
    return user


def create_token():
    user = add_user(firstname='test', lastname='user3',
            email='testuser3@test.com')
    return user.encode_auth_token(user.id).decode()
