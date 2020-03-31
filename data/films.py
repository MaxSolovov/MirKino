import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin


class Films(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    year = sqlalchemy.Column(sqlalchemy.Integer)
    janr = sqlalchemy.Column(sqlalchemy.Integer)
    rejiser = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_serial = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    pict = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    trail = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return '<Film> ' + str(self.id) + ' ' + self.name + ' ' + str(self.year)
