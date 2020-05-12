from datetime import datetime

from app import db


class ResourceMixin(object):
    created_on = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_on = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        """
        Create a human readable version of a class instance.

        :return: self
        """
        obj_id = hex(id(self))
        columns = self.__table__.c.keys()
        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in columns)

        return '<%s %s(%s)>' % (obj_id, self.__class__.__name__, values)
    
    @classmethod
    def find_by_id(cls, id):
        """
        Get a class instance given its id

        :param id: ID
        :type id: int
        :return: Class instance
        """
        return cls.query.get(int(id))

    def save(self):
        """
        Save a model instance.

        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        """
        Delete a model instance.

        :return: db.session.commit()'s result
        """
        db.session.delete(self)
        return db.session.commit()

