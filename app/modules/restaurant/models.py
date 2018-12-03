from app import db
from app.modules.base import Base
from app.modules.orm import ORMClass

# Define a Restaurant model
class Restaurant(Base, ORMClass):

    __tablename__ = 'restaurant'

    # Restaurant fields
    name    = db.Column(db.String(250),  nullable=False)
    address = db.Column(db.String(250), nullable=True)
    tables  = db.relationship('Table', backref='table', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Define a Table model
class Table(Base, ORMClass):

    __tablename__ = 'table_data'

    # Table fields
    capacity      = db.Column(db.Integer, nullable=False)
    minimum       = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id', ondelete='CASCADE'), nullable=False)
