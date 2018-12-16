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

    def get_available_tables(cls, rId):
        bookings_query = Booking.query.with_entities(Booking.table_id).all()
        bookings = [booking for (booking, ) in bookings_query]
        return Table.query.filter(Table.id.notin_(bookings)).filter(Table.restaurant_id == rId).all()

        #sql = "SELECT * FROM table_data WHERE table_data.id NOT IN (SELECT table_id FROM booking) AND table_data.restaurant_id = :id"
        #return db.engine.execute(sql, {'id': rId})

    def get_booked_tables(cls, rId):
        bookings_query = Booking.query.with_entities(Booking.table_id).all()
        bookings = [r for (r, ) in bookings_query]
        return Table.query.filter(Table.id.in_(bookings)).filter(Table.restaurant_id == rId).all()

# Define a Table model
class Table(Base, ORMClass):

    __tablename__ = 'table_data'

    # Table fields
    name          = db.Column(db.String(250), nullable=False)
    capacity      = db.Column(db.Integer, nullable=False)
    minimum       = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    @classmethod
    def check_availability(cls, tId):
        return cls.query.join(Booking).filter(Booking.table_id.in_([tId])).first()


# Define a Booking model
class Booking(Base, ORMClass):

    __tablename__ = 'booking'

    # Booking fields
    email         = db.Column(db.String(250), nullable=False)
    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    table_id      = db.Column(db.Integer, db.ForeignKey('table_data.id'))
