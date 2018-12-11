from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import Required, Email, EqualTo, Length, Optional

# Define the login and sign up forms (WTForms)

class LoginForm(FlaskForm):
    email    = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])


class SignupForm(FlaskForm):
    name     = TextField('Username', [
                Required(message='You need a username')])
    email    = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])


class ChangeUserForm(FlaskForm):
    name     = TextField('name')
    email    = TextField('email', [Email()])
    password = PasswordField('password', [Optional(), Length(min=6, max=35)])


class ChangeUserFormAdmin(FlaskForm):
    name     = TextField('name')
    email    = TextField('email', [Email()])
    password = PasswordField('password', [Optional(), Length(min=6, max=35)])
    role     = SelectField('role', choices=[('1', 'Admin'), ('0', 'User')])
