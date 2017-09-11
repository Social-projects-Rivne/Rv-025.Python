"""Contain a model classes for Booking.
"""

from datetime import datetime

from client_app import db


class Booking(db.Model):

    """Model of booking
    """

    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, default=0, nullable=False)
    reserve_date = db.Column(db.DateTime)
    count_client = db.Column(db.Integer, default=0)
    comment_client = db.Column(db.Text)
    comment_restaurant = db.Column(db.Text)
    client_id = db.Column(
        db.Integer, db.ForeignKey("users.id"))
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurant_restaurant.id"))

    client_id__join = db.relationship(
        "User", foreign_keys="Booking.client_id")
    restaurant_id__join = db.relationship(
        "Restaurant", foreign_keys="Booking.restaurant_id")

    def __init__(self, status, count_client, reserve_date=None):
        self.status = status
        self.count_client = count_client
        if reserve_date is None:
            reserve_date = datetime.utcnow()
        self.reserve_date = reserve_date
