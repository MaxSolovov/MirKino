import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin


class Otziv(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'otzivi'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_film = sqlalchemy.Column(sqlalchemy.Integer)
    id_user = sqlalchemy.Column(sqlalchemy.Integer)
    otziv = sqlalchemy.Column(sqlalchemy.String, nullable=True)


    def __repr__(self):
        return '<Otziv> ' + str(self.id) + str(self.id_film) + ' ' + self.otziv