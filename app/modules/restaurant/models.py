from app import db
from app.modules.base import Base
from app.modules.orm import ORMClass

# Define a Restaurant model
class Restaurant(Base, ORMClass):

    __tablename__ = 'restaurant'

    # Restaurant fields
    name        = db.Column(db.String(250), nullable=False)
    address     = db.Column(db.String(250), nullable=True)
    food        = db.Column(db.String(250), nullable=True)
    tables      = db.relationship('Table', backref='table', cascade="all, delete-orphan", lazy=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def get_available_tables(cls, id):
        return Table.query.join(Booking, Booking.table_id != Table.id).filter(Table.id != Booking.table_id).filter(Table.restaurant_id == id).all()


# Define a Table model
class Table(Base, ORMClass):

    __tablename__ = 'table_data'

    # Table fields
    name          = db.Column(db.String(250), nullable=False)
    capacity      = db.Column(db.Integer, nullable=False)
    minimum       = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    @classmethod
    def check_availability(cls, id):
        return cls.query.join(Booking).filter(Booking.table_id.in_([id])).first()


# Define a Booking model
class Booking(Base, ORMClass):

    __tablename__ = 'booking'

    # Booking fields
    name          = db.Column(db.String(250), nullable=False)
    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'))
    table_id      = db.Column(db.Integer, db.ForeignKey('table_data.id'))
