from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

from orm import ORMClass

engine = create_engine('sqlite:///db/data.db', echo=True)

create_session = sessionmaker(bind=engine)
Session = create_session()

Base = declarative_base(cls=ORMClass)

class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password

    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        Session.add(obj)
        Session.commit()

    """ @classmethod
    def get(cls, id):
        return Session.query(cls).get(id)

    @classmethod
    def all_users(cls):
        q = Session.query(cls).all()
        return q """

# create tables
Base.metadata.create_all(engine)
