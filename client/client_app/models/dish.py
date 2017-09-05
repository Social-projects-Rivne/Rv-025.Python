"""Contain a model classes for dishes and dish categories.
"""

from client_app import db


class Dish(db.Model):

    """Model of Dish object
    """

    __tablename__ = "dish"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey("dish_category.id"))
    name = db.Column(db.String(256))
    photo = db.Column(db.String(256))
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Integer, default=0)
    available = db.Column(db.Boolean, default=True)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurant_restaurant.id"))

    category_id__join = db.relationship(
        "DishCategory", foreign_keys="Dish.category_id")
    restaurant_id__join = db.relationship(
        "Restaurant", foreign_keys="Dish.restaurant_id")


class DishCategory(db.Model):

    """Model of Dish Categories object
    """

    __tablename__ = "dish_category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    is_visible = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
