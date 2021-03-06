#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
User Model
"""

from app import db
from app.modules.base import Base
from app.modules.orm import ORMClass

# Define a User model
class User(Base, ORMClass):
    """ User Class """

    __tablename__ = 'user'

    # User Name
    name = db.Column(db.String(128), nullable=False)

    # Identification Data: email & password
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)

    # Authorisation Data: role & status
    role = db.Column(db.SmallInteger, nullable=False, default=0)
    status = db.Column(db.SmallInteger, nullable=False, default=0)

    restaurants = db.relationship('Restaurant', \
        backref='restaurants', lazy=True)
    bookings = db.relationship('Booking', backref='bookings', lazy=True)

    def __repr__(self):
        return '<User %r>' % (self.name)
