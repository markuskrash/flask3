import csv
import datetime
import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase


class User_bt(SqlAlchemyBase):
    __tablename__ = 'basket'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                               nullable=True)
    drug = sqlalchemy.Column(sqlalchemy.Integer,
                                               nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer,
                                               nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer,
                              nullable=True)

