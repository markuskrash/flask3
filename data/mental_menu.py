import sqlalchemy

from data.db_session import SqlAlchemyBase


class Mental(SqlAlchemyBase):
    __tablename__ = 'mentals'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.INT, nullable=True)