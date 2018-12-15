from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, PasswordField, SelectField
from wtforms.validators import Required, Email, EqualTo, Length, Optional

# Define the restaurants and tables form (WTForms)

class RestaurantFormAdmin(FlaskForm):
    name     = TextField('name', [
                Required(message='Must provide a name.'), Length(min=6, max=35)])
    address  = TextField('address')
    food     = SelectField('food', choices=[('american', 'American'), ('seafood', 'Seafood')])

class TableFormAdmin(FlaskForm):
    name     = TextField('name', [
                Required(message='Must provide a name.'), Length(min=3, max=35)])
    capacity = IntegerField('capacity')
    minimum  = IntegerField('minimum')

class ReservationForm(FlaskForm):
    email    = TextField('email', [Email(),
                Required(message='Forgot your email address?')])
    people   = SelectField('people', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    table    = SelectField('table', coerce=int)