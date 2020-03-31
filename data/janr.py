import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin


class Janr(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'janr'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)


    def __repr__(self):
        return '<Janr> ' + str(self.id) + ' ' + self.name
