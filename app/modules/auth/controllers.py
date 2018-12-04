# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import the require_auth decorator from utils
from app.utils.require_auth import require_auth
from app.utils.require_auth_admin import require_auth_admin

# Import module forms
from app.modules.auth.forms import LoginForm, SignupForm, ChangeUserForm, ChangeUserFormAdmin
from app.modules.restaurant.forms import RestaurantFormAdmin

# Import module models (i.e. User)
from app.modules.auth.models import User
from app.modules.restaurant.models import Restaurant

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@auth.route('/sign-in/', methods=['GET', 'POST'])
def signin():
    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):

            session['user_id'] = user.id
            session['user_role'] = user.role

            flash('Welcome to Chefvenue.io - {}'.format(user.name), 'success-message')

            return redirect(url_for('main'))

        flash('Wrong email or password', 'error-message')

    return render_template('auth/signin.html', form=form)


@auth.route('/sign-up/', methods=['GET', 'POST'])
def signup():
    # If sign up form is submitted
    form = SignupForm(request.form)

    # Verify the sign up form
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            password_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)

            User.create(name=form.name.data, email=form.email.data, password=password_hash)

            return redirect(url_for('auth.signin'))

        flash('User already exists', 'error-message')

    return render_template('auth/signup.html', form=form)


@auth.route('/profile', methods=['GET', 'POST'])
@require_auth
def profile():
    view = request.args.get('view')
    user_id = session.get('user_id')

    if (view == 'change-profile'):
        user_data = User.get(user_id)
        form = ChangeUserForm(request.form, name=user_data.name, email=user_data.email)

        try:
            if form.validate_on_submit():
                user_data.name = form.name.data
                user_data.email = form.email.data
                if (form.password.data == ""):
                    user_data.password = user_data.password

                else:
                    user_data.password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)

                flash('User was updated!', 'success-message')
                # Updated database with new user data
                User.update(user_data)

                return redirect(url_for('auth.profile'))

        except Exception as e:
            flash('Email already exists', 'error-message')

        partial = render_template('auth/profile/change-profile.html', user=user_data, form=form)

    else:
        partial = render_template('auth/profile/reservations.html')

    return render_template('auth/profile/profile.html', render=partial)


@auth.route('/admin', methods=['GET', 'POST'])
@require_auth_admin
def admin():
    view = request.args.get('view')
    action = request.args.get('action')

    if (view == 'restaurants'):
        if (action == 'overview'):
            partial = render_template('auth/admin/restaurants/view.html')

        elif (action == 'add'):
            user_id = session.get('user_id')

            form = RestaurantFormAdmin(request.form)

            try:
                if form.validate_on_submit():

                    restaurant = Restaurant.query.filter_by(name=form.name.data).first()

                    if not restaurant:
                        Restaurant.create(name=form.name.data, address=form.address.data, user_id=user_id)

                        return redirect(url_for('auth.admin', view=['restaurants']))

                    flash('Restaurant already exists', 'error-message')

            except Exception as e:
                print(e)

            partial = render_template('auth/admin/restaurants/add.html', form=form)

        elif (action == 'edit'):
            restaurant_id = request.args.get('restaurantId')
            restaurant_data = Restaurant.get(restaurant_id)

            form = RestaurantFormAdmin(request.form, name=restaurant_data.name, address=restaurant_data.address)

            try:
                if form.validate_on_submit():
                    restaurant_data.name = form.name.data
                    restaurant_data.address = form.address.data

                    flash('Restaurant was updated!', 'success-message')
                    # Updated database with new restaurant data
                    Restaurant.update(restaurant_data)

                    return redirect(url_for('auth.admin', view=['restaurants']))

            except Exception as e:
                print(e)

            partial = render_template('auth/admin/restaurants/edit.html', form=form)

        elif (action == 'delete'):
            restaurant_id = request.args.get('restaurantId')

            restaurant_to_delete = Restaurant.get(restaurant_id)

            if (restaurant_to_delete):
                Restaurant.delete(restaurant_to_delete)

                flash('Restaurant was deleted!', 'success-message')
                return redirect(url_for('auth.admin', view=['restaurants']))

        else:
            # Query all restaurants which an admin has created
            restaurant_list = Restaurant.query.filter(User.role == 1).all()
            partial = render_template('auth/admin/restaurants/restaurants.html', restaurants=restaurant_list)

    else:
        if (action == 'add'):
            form = SignupForm(request.form)

            try:
                if form.validate_on_submit():

                    user = User.query.filter_by(email=form.email.data).first()

                    if not user:
                        password_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)

                        User.create(name=form.name.data, email=form.email.data, password=password_hash)

                        return redirect(url_for('auth.admin', view=['users']))

                    flash('User already exists', 'error-message')

            except Exception as e:
                print(e)

            partial = render_template('auth/admin/users/add.html', form=form)

        elif (action == 'edit'):
            user_id = request.args.get('userId')
            user_data = User.get(user_id)

            form = ChangeUserFormAdmin(request.form, name=user_data.name, email=user_data.email, role=user_data.role)

            try:
                if form.validate_on_submit():
                    user_data.name = form.name.data
                    user_data.email = form.email.data
                    user_data.role = form.role.data
                    if (form.password.data == ""):
                        user_data.password = user_data.password

                    else:
                        user_data.password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)

                    flash('User was updated!', 'success-message')
                    # Updated database with new user data
                    User.update(user_data)

                    return redirect(url_for('auth.admin', view=['users']))

            except Exception as e:
                flash('Email already exists', 'error-message')

            partial = render_template('auth/admin/users/edit.html', user=user_data, form=form)

        elif (action == 'delete'):
            user_id = request.args.get('userId')
            logged_in_user = session.get('user_id')

            user_to_delete = User.get(user_id)

            if (int(logged_in_user) is int(user_id)):
                flash("You can't delete yourself.", 'warning-message')
                return redirect(url_for('auth.admin', view=['users']))

            else:
                User.delete(user_to_delete)
                flash('User was deleted!', 'success-message')
                return redirect(url_for('auth.admin', view=['users']))

        else:
            user_list = User.query.all()
            partial = render_template('auth/admin/users/users.html', users=user_list)

    return render_template('auth/admin/admin.html', render=partial)


@auth.route('/logout/', methods=['GET'])
def logout():
    session.clear()
    flash('You have logged out successfully!', 'success-message')
    return redirect(url_for('main'))
