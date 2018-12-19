#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Restaurant Controllers
"""

# Import flask dependencies
from flask import Blueprint, request, \
    render_template, flash, session, redirect, url_for

# Import the database object from the main app module
#from app import db
from app.utils.binary_search import binary_search
from app.utils.exception_handler import ShowRestaurant, SearchRestaurant

# Import module models (i.e. Restaurant)
from app.modules.auth.models import User
from app.modules.restaurant.models import Restaurant, Booking, Table
from app.modules.restaurant.forms import ReservationForm, SearchForm

# Define the blueprint: 'restaurant', set its url prefix: app.url/restaurant
restaurant = Blueprint('restaurant', __name__, url_prefix='/r')

@restaurant.route('/all', methods=['GET', 'POST'])
def restaurants():
    """ Restaurants Route """
    restaurants_list = Restaurant.query.all()

    return render_template('restaurant/all.html', restaurants=restaurants_list)

@restaurant.route('<int:restaurant_id>', methods=['GET', 'POST'])
def show_restaurant(restaurant_id):
    """ Single Restaurant Route """

    try:
        restaurant_data = Restaurant.get_or_404(restaurant_id)
        available_tables = restaurant_data \
            .get_available_tables(restaurant_data.id)
        user_id = session.get('user_id')
        if user_id:
            user_data = User.get(user_id)
            form = ReservationForm(request.form, email=user_data.email)

        else:
            form = ReservationForm(request.form)

        form.table.choices = [(table.id, table.name.title()) \
            for table in available_tables]

        if form.validate_on_submit():
            table_data = Table.get(form.table.data)

            if int(table_data.capacity) >= int(form.people.data):
                flash('Reservation was created!', 'success-message')

                if user_id:
                    Booking.create(email=form.email.data, \
                        user_id=user_id, table_id=table_data.id)
                    return redirect(url_for('auth.profile'))

                Booking.create(email=form.email.data, table_id=table_data.id)
                return redirect(url_for('restaurant.show_restaurant', \
                    restaurant_id=restaurant_id))

            else:
                flash('Not enought space!', 'warning-message')

        return render_template('restaurant/view.html', \
            restaurant=restaurant_data, form=form)

    except ShowRestaurant:
        return redirect(url_for('restaurant.restaurants'))

@restaurant.route('/search', methods=['GET', 'POST'])
def search():
    """ Search Restaurant Route """

    try:
        restaurants_list = Restaurant.query.order_by("name").all()
        form = SearchForm(request.form)
        message = ""

        if form.validate_on_submit():
            query = form.query.data

            result = binary_search(restaurants_list, query)

            if result is None:
                restaurants_list = []
                message = "No results found"
            else:
                restaurants_list = result
                message = ""

        return render_template('restaurant/search.html', form=form, \
            restaurants=restaurants_list, message=message)

    except SearchRestaurant:
        return redirect(url_for('restaurant.search'))
