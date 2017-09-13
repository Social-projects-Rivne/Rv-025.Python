"""Contain a model classes for Booking.
"""

from client_app import db


class Booking(db.Model):

    """Model of booking

    BOOKING_STATUS:
        0 = New
        1 = Pending
        2 = OK
        3 = Canceled by Admin
        4 = Canceled by User

    Arguments:
        id = primary key of booking record
        status = status of booked record, stored in DB
        statuses = list of user-friendly statuses
        status_friendly() = method that convert 'status id' into word
        reserve_date = date of reservation
        count_client = Clients count
        comment_client = Client comment
        comment_restaurant = Admin of Restaurant comment
        client_id = User/Client id
        restaurant_id = Restaurant id
    """

    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, default=0, nullable=False)
    reserve_date = db.Column(db.DateTime, nullable=True)
    count_client = db.Column(db.Integer, default=0)
    comment_client = db.Column(db.Text, nullable=True)
    comment_restaurant = db.Column(db.Text, nullable=True)
    client_id = db.Column(
        db.Integer, db.ForeignKey("users.id"))
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurant_restaurant.id"))

    client_id__join = db.relationship(
        "User", foreign_keys="Booking.client_id")
    restaurant_id__join = db.relationship(
        "Restaurant", foreign_keys="Booking.restaurant_id")

    statuses = ['New', 'Pending', 'OK', 'Canceled by Admin',
                'Canceled by User']

    @classmethod
    def create(cls, status, reserve_date, count_client, comment_client,
               client_id, restaurant_id):
        model = cls()
        model.status = status
        model.reserve_date = reserve_date
        model.count_client = count_client
        model.comment_client = comment_client
        model.client_id = client_id
        model.restaurant_id = restaurant_id
        return model

    def status_friendly(self):
        return self.statuses[int(self.status)]
