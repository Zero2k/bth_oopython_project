#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

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

@app.route('/')
def main():
    return render_template("home.html")

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', title="Page Not Found"), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.modules.auth.controllers import auth as auth_module

# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()