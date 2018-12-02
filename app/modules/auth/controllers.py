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
from app.modules.auth.forms import LoginForm, SignupForm, ChangeUserForm

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
    user_data = User.get(session.get('user_id'))

    if (view == 'change-profile'):
        # If change user form is submitted
        form = ChangeUserForm(request.form, email=user_data.email)

        # Verify the user change form
        if form.validate_on_submit():
            user_data.email = form.email.data
            if (form.password.data == ""):
                user_data.password = user_data.password

            else:
                user_data.password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)

            # Updated database with new user data
            User.update(user_data)

            return redirect(url_for('auth.profile'))

        partial = render_template('auth/profile/change-profile.html', user=user_data, form=form)

    else:
        partial = render_template('auth/profile/reservations.html')

    return render_template('auth/profile/profile.html', render=partial, user=user_data)


@auth.route('/admin', methods=['GET', 'POST'])
@require_auth_admin
def admin():
    view = request.args.get('view')
    action = request.args.get('action')

    if (view == 'resturants'):
        if (action == 'add'):
            partial = render_template('auth/admin/resturants/add.html')

        else:
            # Query all restaurants which an admin has created
            restaurant_list = Restaurant.query.filter(User.role == 1).all()
            partial = render_template('auth/admin/resturants/resturants.html', restaurants=restaurant_list)

    else:
        if (action == 'add'):
            partial = render_template('auth/admin/users/add.html')

        else:
            user_list = User.query.all()
            partial = render_template('auth/admin/users/users.html', users=user_list)

    return render_template('auth/admin/admin.html', render=partial)


@auth.route('/logout/', methods=['GET'])
def logout():
    session.clear()
    flash('You have logged out successfully!', 'success-message')
    return redirect(url_for('main'))
