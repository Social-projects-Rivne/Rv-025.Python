"""Form for Booking request
"""

from flask_wtf import FlaskForm
from wtforms import IntegerField, HiddenField, StringField, \
                    SubmitField, TextAreaField
from wtforms.widgets.html5 import NumberInput


class BookingForm(FlaskForm):
    """
    status = 1 = "pending approval"
    """

    client_id = HiddenField('user_id', default='')
    status = HiddenField('status', default=1)
    restaurant_id = HiddenField('restaurant_id', default='')

    reserve_date = StringField('Date and Time')
    count_client = IntegerField('Count of Clients', widget=NumberInput())
    comment_client = TextAreaField("Comment")
    submit = SubmitField("Send")
