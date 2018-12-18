#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Auth Controllers
"""

# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
#from app import db

# Import the require_auth decorator from utils
from app.utils.require_auth import require_auth
from app.utils.require_auth_admin import require_auth_admin

# Import module forms
from app.modules.auth.forms import LoginForm, SignupForm, \
    ChangeUserForm, ChangeUserFormAdmin
from app.modules.restaurant.forms import RestaurantFormAdmin, TableFormAdmin

# Import module models (i.e. User)
from app.modules.auth.models import User
from app.modules.restaurant.models import Restaurant, Table, Booking

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@auth.route('/sign-in/', methods=['GET', 'POST'])
def signin():
    """ Sign in Route """
    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user and check_password_hash(user.password, form.password.data):

            session['user_id'] = user.id
            session['user_role'] = user.role

            flash('Welcome to Chefvenue.io - {}'.format(user.name), \
                'success-message')

            return redirect(url_for('main'))

        flash('Wrong email or password', 'error-message')

    return render_template('auth/signin.html', form=form)


@auth.route('/sign-up/', methods=['GET', 'POST'])
def signup():
    """ Sign up Route """
    # If sign up form is submitted
    form = SignupForm(request.form)

    # Verify the sign up form
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data.lower()).first()

        if not user:
            password_hash = generate_password_hash(form.password.data, \
                method='pbkdf2:sha256', salt_length=8)

            User.create(name=form.name.data.lower(), \
                email=form.email.data.lower(), password=password_hash)

            return redirect(url_for('auth.signin'))

        flash('User already exists', 'error-message')

    return render_template('auth/signup.html', form=form)


@auth.route('/profile', methods=['GET', 'POST'])
@require_auth
def profile():
    """ Profile Route """
    view = request.args.get('view')
    action = request.args.get('action')
    user_id = session.get('user_id')

    if view == 'change-profile':
        user_data = User.get(user_id)
        form = ChangeUserForm(request.form, name=user_data.name, \
            email=user_data.email)

        try:
            if form.validate_on_submit():
                user_data.name = form.name.data.lower()
                user_data.email = form.email.data.lower()
                if form.password.data == "":
                    user_data.password = user_data.password

                else:
                    user_data.password = generate_password_hash( \
                        form.password.data, \
                        method='pbkdf2:sha256', \
                        salt_length=8)

                flash('User was updated!', 'success-message')
                # Updated database with new user data
                User.update(user_data)

                return redirect(url_for('auth.profile'))

        except Exception as e:
            flash('Email already exists', 'error-message')

        partial = render_template('auth/profile/change-profile.html', \
            user=user_data, form=form)

    else:
        # Delete booking
        if action == 'delete':
            booking_id = request.args.get('bookingId')

            try:
                booking_to_delete = Booking.get(booking_id)

                if booking_to_delete:
                    Booking.delete(booking_to_delete)

                    flash('Booking was deleted!', 'success-message')
                    return redirect(url_for('auth.profile', \
                        view=['reservations']))

            except Exception as e:
                print(e)

        else:
            my_reservations = Booking.query \
                .filter(Booking.user_id == user_id).all()
            #user_data = User.get(user_id)
            #my_reservations2 = user_data.bookings
            #print(my_reservations2)
            partial = render_template('auth/profile/reservations.html', \
                reservations=my_reservations)

    return render_template('auth/profile/profile.html', render=partial)


@auth.route('/admin', methods=['GET', 'POST'])
@require_auth_admin
def admin():
    """ Admin Route """
    view = request.args.get('view')
    action = request.args.get('action')
    sort = request.args.get('sort')

    if view == 'restaurants':
        # View restaurant
        if action == 'overview':
            restaurant_id = request.args.get('restaurantId')
            restaurant_data = Restaurant.get(restaurant_id)

            # Filter restaurant reservations
            if sort == 'booked':
                table_list = restaurant_data \
                    .get_booked_tables(restaurant_data.id)
            elif sort == 'available':
                table_list = restaurant_data \
                    .get_available_tables(restaurant_data.id)
            else:
                table_list = Table.query \
                    .filter(Table.restaurant_id == restaurant_id).all()

            partial = render_template('auth/admin/restaurants/view.html', \
                restaurant=restaurant_data, tables=table_list)

        # Add table
        elif action == 'add-table':
            restaurant_id = request.args.get('restaurantId')

            form = TableFormAdmin(request.form)

            try:
                if form.validate_on_submit():
                    Table.create(name=form.name.data.lower(), \
                        capacity=form.capacity.data, \
                        minimum=form.minimum.data, restaurant_id=restaurant_id)

                    flash('Table was created!', 'success-message')
                    return redirect(url_for('auth.admin', \
                        view=['restaurants']))

            except Exception as e:
                print(e)

            partial = render_template( \
                'auth/admin/restaurants/tables/add.html', form=form)

        # Edit table
        elif action == 'edit-table':
            table_id = request.args.get('tableId')
            table_data = Table.get(table_id)

            form = TableFormAdmin(request.form, name=table_data.name, \
                capacity=table_data.capacity, minimum=table_data.minimum)

            try:
                if form.validate_on_submit():
                    table_data.name = form.name.data.lower()
                    table_data.capacity = form.capacity.data.lower()
                    table_data.minimum = form.minimum.data.lower()
                    flash('Table was updated!', 'success-message')
                    # Updated database with new table data
                    Table.update(table_data)

                    return redirect(url_for('auth.admin', \
                        view=['restaurants']))

            except Exception as e:
                print(e)

            partial = render_template( \
                'auth/admin/restaurants/tables/edit.html', form=form)

        # Delete table
        elif action == 'delete-table':
            table_id = request.args.get('tableId')

            try:
                table_to_delete = Table.get(table_id)

                if table_to_delete:
                    Table.delete(table_to_delete)

                    flash('Table was deleted!', 'success-message')
                    return redirect(url_for('auth.admin', \
                        view=['restaurants']))

            except Exception as e:
                print(e)

        # Add restaurant
        elif action == 'add':
            user_id = session.get('user_id')

            form = RestaurantFormAdmin(request.form)

            try:
                if form.validate_on_submit():

                    restaurant = Restaurant.query \
                        .filter_by(name=form.name.data.lower()).first()

                    if not restaurant:
                        Restaurant.create(name=form.name.data.lower(), \
                            address=form.address.data.lower(), \
                            food=form.food.data.lower(), user_id=user_id)

                        return redirect(url_for('auth.admin', \
                            view=['restaurants']))

                    flash('Restaurant already exists', 'error-message')

            except Exception as e:
                print(e)

            partial = render_template( \
                'auth/admin/restaurants/add.html', form=form)

        # Edit restaurant
        elif action == 'edit':
            restaurant_id = request.args.get('restaurantId')
            restaurant_data = Restaurant.get(restaurant_id)

            form = RestaurantFormAdmin(request.form, \
                name=restaurant_data.name, address=restaurant_data.address, \
                food=restaurant_data.food)

            try:
                if form.validate_on_submit():
                    restaurant_data.name = form.name.data.lower()
                    restaurant_data.address = form.address.data.lower()
                    restaurant_data.food = form.food.data.lower()

                    flash('Restaurant was updated!', 'success-message')
                    # Updated database with new restaurant data
                    Restaurant.update(restaurant_data)

                    return redirect(url_for('auth.admin', \
                        view=['restaurants']))

            except Exception as e:
                print(e)

            partial = render_template( \
                'auth/admin/restaurants/edit.html', form=form)

        # Delete restaurant
        elif action == 'delete':
            restaurant_id = request.args.get('restaurantId')

            try:
                restaurant_to_delete = Restaurant.get(restaurant_id)

                if restaurant_to_delete:
                    Restaurant.delete(restaurant_to_delete)

                    flash('Restaurant was deleted!', 'success-message')
                    return redirect(url_for('auth.admin', \
                        view=['restaurants']))

            except Exception as e:
                print(e)

        else:
            # Query all restaurants which an admin has created
            restaurant_list = Restaurant.query.filter(User.role == 1).all()
            partial = render_template( \
                'auth/admin/restaurants/restaurants.html', \
                restaurants=restaurant_list)

    elif view == 'reservations':
        # Delete reservations
        if action == 'delete':
            booking_id = request.args.get('bookingId')

            try:
                booking_to_delete = Booking.get(booking_id)

                if booking_to_delete:
                    Booking.delete(booking_to_delete)

                    flash('Booking was deleted!', 'success-message')
                    return redirect(url_for('auth.admin', \
                    view=['reservations']))

            except Exception as e:
                print(e)

        # View all reservations
        else:
            reservation_list = Booking.query.all()
            partial = render_template( \
                'auth/admin/reservations/reservations.html', \
                reservations=reservation_list)

    else:
        # Add user
        if action == 'add':
            form = SignupForm(request.form)

            try:
                if form.validate_on_submit():

                    user = User.query \
                        .filter_by(email=form.email.data).first()

                    if not user:
                        password_hash = generate_password_hash( \
                            form.password.data, \
                            method='pbkdf2:sha256', \
                            salt_length=8)

                        User.create(name=form.name.data, \
                            email=form.email.data, \
                            password=password_hash)

                        return redirect(url_for('auth.admin', view=['users']))

                    flash('User already exists', 'error-message')

            except Exception as e:
                print(e)

            partial = render_template('auth/admin/users/add.html', form=form)

        # Edit user
        elif action == 'view':
            user_id = request.args.get('userId')
            user_data = User.get(user_id)

            partial = render_template( \
                'auth/admin/users/view.html', user=user_data)

        # Edit user
        elif action == 'edit':
            user_id = request.args.get('userId')
            user_data = User.get(user_id)

            form = ChangeUserFormAdmin(request.form, name=user_data.name, \
                email=user_data.email, role=user_data.role)

            try:
                if form.validate_on_submit():
                    user_data.name = form.name.data.lower()
                    user_data.email = form.email.data.lower()
                    user_data.role = form.role.data.lower()
                    if form.password.data == "":
                        user_data.password = user_data.password

                    else:
                        user_data.password = generate_password_hash( \
                            form.password.data, \
                            method='pbkdf2:sha256', \
                            salt_length=8)

                    flash('User was updated!', 'success-message')
                    # Updated database with new user data
                    User.update(user_data)

                    return redirect(url_for('auth.admin', view=['users']))

            except Exception as e:
                flash('Email already exists', 'error-message')

            partial = render_template( \
                'auth/admin/users/edit.html', user=user_data, form=form)

        # Delete user
        elif action == 'delete':
            user_id = request.args.get('userId')
            logged_in_user = session.get('user_id')

            try:
                user_to_delete = User.get(user_id)

                if int(logged_in_user) is int(user_id):
                    flash("You can't delete yourself.", 'warning-message')
                    return redirect(url_for('auth.admin', view=['users']))

                User.delete(user_to_delete)
                flash('User was deleted!', 'success-message')
                return redirect(url_for('auth.admin', view=['users']))

            except Exception as e:
                print(e)

        else:
            user_list = User.query.all()
            partial = render_template( \
                'auth/admin/users/users.html', users=user_list)

    return render_template('auth/admin/admin.html', render=partial)


@auth.route('/logout/', methods=['GET'])
def logout():
    """ Logout Route """
    session.clear()
    flash('You have logged out successfully!', 'success-message')
    return redirect(url_for('main'))
