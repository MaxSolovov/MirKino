import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin


class Reiting(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'reiting'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_film = sqlalchemy.Column(sqlalchemy.Integer)
    bal = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)


    def __repr__(self):
        return '<Janr> ' + str(self.id) + ' ' + self.name