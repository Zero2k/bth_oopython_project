#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Restaurant Forms
"""

from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, SelectField
from wtforms.validators import Required, Email, Length

# Define the restaurants and tables form (WTForms)

class RestaurantFormAdmin(FlaskForm):
    """ Restaurant Form (Admin) """
    name = TextField('name', [
        Required(message='Must provide a name.'), Length(min=6, max=35)])
    address = TextField('address')
    food = SelectField('food', choices=[ \
        ('american', 'American'), ('seafood', 'Seafood'), \
        ('steakhouse', 'Steakhouse'), ('italian', 'Italian')])

class TableFormAdmin(FlaskForm):
    """ Table Form (Admin) """
    name = TextField('name', [
        Required(message='Must provide a name.'), Length(min=3, max=35)])
    capacity = IntegerField('capacity')
    minimum = IntegerField('minimum')

class ReservationForm(FlaskForm):
    """ Reservation Form """
    email = TextField('email', [Email(), Required( \
        message='Forgot your email address?')])
    people = SelectField('people', choices=[('1', '1'), ('2', '2'), \
        ('3', '3'), ('4', '4')])
    table = SelectField('table', coerce=int)
