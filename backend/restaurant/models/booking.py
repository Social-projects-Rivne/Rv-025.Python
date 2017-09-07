"""
Contain a model class for booking.
"""

from django.db import models

from administrator.models import User
from restaurant import Restaurant


class Booking(models.Model):

    """Model of Booking
    """

    STATUS_NEW = 0
    STATUS_PENDING = 1
    STATUS_OK = 2
    STATUS_CANCELED = 3

    BOOKING_STATUS = (
        (STATUS_NEW, "new"),
        (STATUS_PENDING, "pending"),
        (STATUS_OK, "ok"),
        (STATUS_CANCELED, "canceled"),
    )

    status = models.IntegerField(choices=BOOKING_STATUS, default=0)
    reserve_date = models.DateTimeField(blank=True)
    count_client = models.IntegerField(default=0)
    count_tables = models.IntegerField(default=1, null=False)
    comment_client = models.TextField(blank=True)
    comment_restaurant = models.TextField(blank=True)
    client = models.ForeignKey(User, null=False)
    restaurant = models.ForeignKey(Restaurant, null=False)

    class Meta():

        """Give some options attached to the model."""

        db_table = 'booking'
        verbose_name_plural = 'Booking'
        permissions = (
            ('read_booking', 'Can read information about booking'),
        )
