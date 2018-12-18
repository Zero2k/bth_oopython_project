#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Class Base
"""

from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
    """ Base Class """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, \
        default=db.func.current_timestamp(), \
        onupdate=db.func.current_timestamp())
