# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Import module forms

# Import module models (i.e. Restaurant)
from app.modules.restaurant.models import Restaurant

# Define the blueprint: 'restaurant', set its url prefix: app.url/restaurant
restaurant = Blueprint('restaurant', __name__, url_prefix='/r')

@restaurant.route('/all/', methods=['GET', 'POST'])
def restaurants():
    restaurants_list = Restaurant.query.all()

    return render_template('restaurant/all.html', restaurants=restaurants_list)

@restaurant.route('<int:restaurant_id>', methods=['GET'])
def show_restaurant(restaurant_id):

    try:
        restaurant = Restaurant.get_or_404(restaurant_id)

        return render_template('restaurant/view.html', restaurant=restaurant)

    except Exception as e:
        return redirect(url_for('restaurant.restaurants'))
