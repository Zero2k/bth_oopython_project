# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Import module models (i.e. Restaurant)
from app.modules.auth.models import User
from app.modules.restaurant.models import Restaurant, Booking
from app.modules.restaurant.forms import ReservationForm

# Define the blueprint: 'restaurant', set its url prefix: app.url/restaurant
restaurant = Blueprint('restaurant', __name__, url_prefix='/r')

@restaurant.route('/all/', methods=['GET', 'POST'])
def restaurants():
    restaurants_list = Restaurant.query.all()

    return render_template('restaurant/all.html', restaurants=restaurants_list)

@restaurant.route('<int:restaurant_id>', methods=['GET', 'POST'])
def show_restaurant(restaurant_id):

    try:
        restaurant_data = Restaurant.get_or_404(restaurant_id)
        available_tables = restaurant_data.get_available_tables(restaurant_data.id)
        user_id = session.get('user_id')
        if (user_id):
            user_data = User.get(user_id)
            form = ReservationForm(request.form, email=user_data.email)

        else:
            form = ReservationForm(request.form)

        form.table.choices = [(table.id, table.name.title()) for table in available_tables]

        if form.validate_on_submit():
            print(form.data)
            flash('Reservation was created!', 'success-message')
            return redirect(url_for('auth.profile'))

        return render_template('restaurant/view.html', restaurant=restaurant_data, form=form)

    except Exception as e:
        return redirect(url_for('restaurant.restaurants'))
