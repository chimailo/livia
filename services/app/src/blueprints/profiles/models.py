from hashlib import md5
from random import random

from src import db
from src.utils.models import ResourceMixin


class Profile(db.Model, ResourceMixin):
    __tablename__ = 'profiles'

    # Identification
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32), index=True, nullable=False)
    lastname = db.Column(db.String(32), index=True, nullable=False)
    username = db.Column(
        db.String(128),
        index=True,
        unique=True,
        nullable=False
    )
    bio = db.Column(db.String(255))
    avatar = db.Column(db.String(128))
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    def __repr__(self):
        return f'<Profile: {self.id} | {self.firstname} | {self.lastname}>'

    @classmethod
    def find_by_username(cls, username):
        """
        Find a profile by its username.

        :param: username
        :return: Profile instance
        """
        return cls.query.filter(cls.username == username).first()

    def set_username(self):
        digits = str(random()*1e5).split('.')[0]
        return f'{self.firstname.lower()}{self.lastname.lower()}_{digits}'

    @staticmethod
    def set_avatar(email, size=128):
        digest = md5(email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?s={size}&d=mm&r=pg'
