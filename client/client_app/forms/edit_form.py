"""
Contain a model class for user edit.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class EditForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(EditForm, self).__init__(*args, **kwargs)

    name = StringField('name', [
        validators.DataRequired(),
        validators.Length(max=50)
    ])
    phone = StringField('phone', [
        validators.Length(max=12)
    ])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Length(min=8),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', [
        validators.DataRequired()
    ])
