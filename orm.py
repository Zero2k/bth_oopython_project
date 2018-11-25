from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker

engine = create_engine('sqlite:///db/data.db', echo=True)

create_session = sessionmaker(bind=engine)
Session = create_session()

class ORMClass(object):
    @classmethod
    def query(class_):
        return Session.query(class_).all()

    @classmethod
    def get_by_id(class_, id):
        return Session.query(class_).get(id)

    @classmethod
    def get_by_query(class_, query):
        return Session.query(class_).filter(query).all()

