"""Contain a model classes for restaurant and restaurant type.
"""

from client_app import db


class Restaurant(db.Model):

    """Model of Restaurant object
    """

    __tablename__ = 'restaurant_restaurant'

    STATUS_ACTIVE = 0
    STATUS_DELETED = 1
    STATUS_HIDDEN = 2

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    logo = db.Column(db.String(256), default="Logo_added")
    location = db.Column(db.String(256))
    restaurant_type_id = db.Column(db.Integer,
                                   db.ForeignKey('restaurant_restauranttype.id'))
    status = db.Column(db.Integer, default=STATUS_ACTIVE, nullable=False)
    tables_count = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    manager_id = db.Column(db.Integer)
    sub_manager_id = db.Column(db.Integer)

    restaurant_type = db.relationship('RestaurantType',
                                      foreign_keys="Restaurant.restaurant_type_id")


class RestaurantType(db.Model):

    """Restaurants Type model
    """

    __tablename__ = 'restaurant_restauranttype'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_type = db.Column(db.String(256), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def __init__(self, id, restaurant_type, is_deleted):
        self.id = id
        self.restaurant_type = restaurant_type
        self.is_deleted = is_deleted

    def __repr__(self):
        return self.restaurant_type
