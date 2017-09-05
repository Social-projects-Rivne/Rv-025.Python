"""
Contain a model class for user login.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField(
        'email',
        validators=[InputRequired(), Email('Invalid Email')]
    )
    password = PasswordField(
        'password',
        validators=[InputRequired(), Length(min=8)]
    )
