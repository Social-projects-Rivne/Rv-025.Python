"""
Contain a model class for user login.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    email = StringField(
        'email', id='login_email',
        validators=[InputRequired()]
    )
    password = PasswordField(
        'password',id='login_password',
        validators=[InputRequired()]
    )
