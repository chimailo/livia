from src import db
from src.utils.models import ResourceMixin


class Team(db.Model, ResourceMixin):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, nullable=False, unique=True)
    about = db.Column(db.String(255))
    avatar = db.Column(db.String(64))
