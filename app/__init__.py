#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" Init App """

# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

from app.modules.restaurant.models import Restaurant

@app.route('/')
def main():
    """ Render home page """
    restaurants_list = Restaurant.query.limit(6).all()

    return render_template("home.html", restaurants=restaurants_list)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found():
    """ Render 404 page """
    return render_template('404.html', title="Page Not Found"), 404

# Import a modules / components using its blueprint handler variable
from app.modules.auth.controllers import auth as auth_module
from app.modules.restaurant.controllers import restaurant as restaurant_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(restaurant_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
