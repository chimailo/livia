from datetime import datetime, timedelta
import jwt

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from src import db
from src.utils.models import ResourceMixin


users_teams = db.Table(
    'users_teams',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    ),
    db.Column(
        'team_id',
        db.Integer,
        db.ForeignKey('teams.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
)


class User(db.Model, ResourceMixin):
    __tablename__ = 'users'

    # Identification
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(
        db.String(128),
        index=True,
        unique=True,
        nullable=False
    )
    password = db.Column(db.String(128), nullable=False)

    # Authorization
    is_active = db.Column(db.Boolean(), default=True, nullable=False)
    is_admin = db.Column(db.Boolean(), default=False, nullable=False)

    # Activity tracking.
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(db.DateTime)
    current_sign_in_ip = db.Column(db.String(32))
    last_sign_in_on = db.Column(db.DateTime)
    last_sign_in_ip = db.Column(db.String(32))

    # Relationships
    profile = db.relationship(
        'Profile',
        uselist=False,
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )
    teams = db.relationship(
        'Team',
        lazy='dynamic',
        secondary=users_teams,
        backref=db.backref('members', lazy='dynamic')
    )

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = User.hash_password(kwargs.get('password', ''))

    def __str__(self):
        return f'<User {self.id} {self.email}>'

    @classmethod
    def find_by_email(cls, email):
        """
        Find a user by their email.

        :param: email
        :return: User instance
        """
        return cls.query.filter(cls.email == email).first()

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
            return payload.get('sub')
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def update_activity_tracking(self, ip_address):
        """
        Update various fields on the user that's related to meta data on
        their account, such as the sign in count and ip address, etc..

        :param ip_address: IP address
        :type ip_address: str
        :return: SQLAlchemy commit results
        """
        self.sign_in_count += 1

        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_on = datetime.utcnow()
        self.current_sign_in_ip = ip_address

        return self.save()
