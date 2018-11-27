from app import db
from app.modules.orm import ORMClass

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Define a User model
class User(Base, ORMClass):

    __tablename__ = 'user'

    # User Name
    name    = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email    = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.name     = name
        self.email    = email
        self.password = password
        self.role     = 0
        self.status   = 0

    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % (self.name)  
