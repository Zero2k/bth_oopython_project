# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.modules.auth.forms import LoginForm, SignupForm

# Import module models (i.e. User)
from app.modules.auth.models import User

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

            return redirect(url_for('main'))

        flash('Wrong email or password', 'error-message')

    return render_template("auth/signin.html", form=form)


@auth.route('/sign-up/', methods=['GET', 'POST'])
def signup():

    # If sign up form is submitted
    form = SignupForm(request.form)

    # Verify the sign up form
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            passwordHash = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)

            User.create(name=form.name.data, email=form.email.data, password=passwordHash)

            return redirect(url_for('auth.signin'))

        else:
            flash('User already exists', 'error-message')

    return render_template("auth/signup.html", form=form)


@auth.route('/logout/', methods=['GET'])
def logout():

    session.clear()
    return redirect(url_for('main'))
