"""
Contain a model class for dishes.
"""
from django.db import models

import restaurant
from dish_category import DishCategory


class Dish(models.Model):

    """Model of dish, creates from manager panel."""

    category = models.ForeignKey(DishCategory,
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    name = models.CharField(max_length=100, default='', null=False)
    photo = models.ImageField(upload_to='dish_images', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    weight = models.IntegerField(default=0, null=False)
    available = models.BooleanField(default=True)
    restaurant = models.ForeignKey(restaurant.Restaurant,
                                   on_delete=models.CASCADE,
                                   default=0, null=False)

    class Meta():

        """Give some options attached to the model."""

        db_table = 'dish'
        verbose_name_plural = 'Dishes'
        permissions = (
            ('read_dish', 'Can read information about dish'),
        )

    def is_available(self, available):
        """Set dish available or not status.

        Argument:
        available (boolean) - status of dish in menu
        """
        self.available = (available == 1)

    def __str__(self):
        return self.name
