from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

from client_app import db
from client_app.models.user import User


def unique_email(form, field):
    if (db.session.query(User.id).filter_by(email=field.data).scalar() is not
            None):
        raise validators.ValidationError('User with this email already exists')


class RegistrationForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(RegistrationForm, self).__init__(*args, **kwargs)

    name = StringField('Name', [
        validators.Length(max=50),
        validators.DataRequired()
    ])
    email = StringField('Email', [
        validators.Length(max=120),
        validators.Email('Enter correct email, please'),
        validators.DataRequired(),
        unique_email
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=8),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Password (again):', [validators.DataRequired()])
