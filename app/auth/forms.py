from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.auth.validators import UniqueUsername, UniqueEmail

class LoginForm(FlaskForm):
    """
    Form for users to log in.
    """
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Enter a valid email address.'),
        Length(max=120, message='Email must be less than 120 characters.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.')
    ])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    """
    Form for users to create a new account.
    """
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=2, max=50, message='Username must be between 2 and 50 characters.'),
        UniqueUsername()
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Enter a valid email address.'),
        Length(max=120, message='Email must be less than 120 characters.'),
        UniqueEmail()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password.'),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')

