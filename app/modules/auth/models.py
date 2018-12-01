from app import db
from app.modules.base import Base
from app.modules.orm import ORMClass

# Define a User model
class User(Base, ORMClass):

    __tablename__ = 'user'

    # User Name
    name    = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email    = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False, default=0)
    status   = db.Column(db.SmallInteger, nullable=False, default=0)

    """ @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit() """

    """ @classmethod
    def update(cls, obj):
        db.session.add(obj)
        db.session.commit() """

    def __repr__(self):
        return '<User %r>' % (self.name)  
