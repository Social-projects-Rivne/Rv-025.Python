"""
Contain a model class for user edit.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators



def password_check(form, field):
    if field.data and len(field.data) < 7:
        raise validators.ValidationError('Field must be more than 8 characters')


class EditForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(EditForm, self).__init__(*args, **kwargs)

    name = StringField('Name', [
        validators.DataRequired(),
        validators.Length(max=50)
    ])
    phone = StringField('Phone', [
        validators.Length(max=12)
    ])
    password = PasswordField('New Password', [
        #validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        password_check
    ])
    confirm = PasswordField('Repeat Password', [
        #validators.DataRequired()
    ])
