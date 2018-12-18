#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Restaurant Models
"""

from app import db
from app.modules.base import Base
from app.modules.orm import ORMClass

# Define a Restaurant model
class Restaurant(Base, ORMClass):
    """ Restaurant Class """

    __tablename__ = 'restaurant'

    # Restaurant fields
    name = db.Column(db.String(250), nullable=False)
    address = db.Column(db.String(250), nullable=True)
    food = db.Column(db.String(250), nullable=True)
    tables = db.relationship('Table', backref='tables', \
        cascade="all, delete-orphan", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @classmethod
    def get_available_tables(cls, restaurant_id):
        """ Get available tables """
        bookings_query = Booking.query.with_entities(Booking.table_id).all()
        bookings = [booking for (booking, ) in bookings_query]
        return Table.query.filter(Table.id.notin_(bookings)) \
            .filter(Table.restaurant_id == restaurant_id).all()

    @classmethod
    def get_booked_tables(cls, restaurant_id):
        """ Get bokked tables """
        bookings_query = Booking.query.with_entities(Booking.table_id).all()
        bookings = [r for (r, ) in bookings_query]
        return Table.query.filter(Table.id.in_(bookings)) \
            .filter(Table.restaurant_id == restaurant_id).all()

# Define a Table model
class Table(Base, ORMClass):
    """ Table Class """

    __tablename__ = 'table_data'

    # Table fields
    name = db.Column(db.String(250), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    minimum = db.Column(db.Integer, nullable=False)
    restaurant = db.relationship('Restaurant', backref='restaurant', \
        lazy=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    @classmethod
    def check_availability(cls, table_id):
        """ Check table availability """
        return cls.query.join(Booking) \
            .filter(Booking.table_id.in_([table_id])).first()


# Define a Booking model
class Booking(Base, ORMClass):
    """ Booking Class """

    __tablename__ = 'booking'

    # Booking fields
    email = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    table = db.relationship('Table', backref='table', \
        lazy=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table_data.id'))
