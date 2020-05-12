from datetime import datetime, timedelta
from hashlib import md5
import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.utils.models import ResourceMixin


# user_groups = db.Table(
#     'user_groups',
#     db.Column(
#         'user_id',
#         db.Integer,
#         db.ForeignKey('users.id'),
#         primary_key=True
#     ),
#     db.Column(
#         'group_id',
#         db.Integer,
#         db.ForeignKey('groups.id'),
#         primary_key=True
#     )
# )


class User(db.Model, ResourceMixin):
    __tablename__ = 'users'

    # Identification
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    username = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(128), nullable=False)

    firstname = db.Column(db.String(32), index=True)
    lastname = db.Column(db.String(32), index=True)
    bio = db.Column(db.String(255))

    # Authorization
    is_active = db.Column(db.Boolean(), default=True, nullable=False)
    is_admin = db.Column(db.Boolean(), default=False, nullable=False)

    # Activity tracking.
    created_on = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(db.DateTime)
    current_sign_in_ip = db.Column(db.String(32))
    last_sign_in_on = db.Column(db.DateTime)
    last_sign_in_ip = db.Column(db.String(32))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = User.hash_password(kwargs.get('password', ''))

    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a user by their email or username.

        :param identity: Email or Username
        :type identity: str
        :return: User instance
        """
        return cls.query.filter(
            (cls.email == identity) | (cls.username == identity)
        ).first()

    @classmethod
    def hash_password(cls, password):
        """
        Hash a plaintext string using PBKDF2.

        :param password: Password in plain text
        :type password: str
        :return: str
        """
        if password:
            return generate_password_hash(password)

        return None

    def check_password(self, password):
        """
        Check if the provided password matches that of the specified user.

        :param password: Password in plain text
        :return: boolean
        """
        return check_password_hash(self.password, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?s={size}&d=mm&r=pg'

    def encode_auth_token(self, id):
        """Generates the auth token"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.utcnow(),
                'sub': {
                    'id': id,
                }
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        """
        Decodes the auth token

        :param string: token
        :return dict: The user's identity
        """
        try:
            payload = jwt.decode(
                token,
                current_app.config.get('SECRET_KEY'),
                algorithms='HS256'
            )
            print(payload.get('sub'))
            return payload.get('sub')
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def update_activity_tracking(self):
        """
        Update various fields on the user that's related to meta data on
        their account, such as the sign in count and ip address, etc..

        :param ip_address: IP address
        :type ip_address: str
        :return: SQLAlchemy commit results
        """
        self.sign_in_count += 1

        self.last_sign_in_on = self.current_sign_in_on
        # self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_on = datetime.utcnow()
        # self.current_sign_in_ip = ip_address

        return self.save()
