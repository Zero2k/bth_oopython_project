# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Import module forms

# Import module models (i.e. Restaurant)
from app.modules.restaurant.models import Restaurant

# Define the blueprint: 'restaurant', set its url prefix: app.url/restaurant
restaurant = Blueprint('restaurant', __name__, url_prefix='/restaurant')
