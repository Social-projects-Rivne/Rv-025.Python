"""
Contain a model class for dishes.
"""
from django.db import models

from administrator.models import dish_category


class Dish(models.Model):

    """Model of dish, creates from manager panel."""

    category = models.ForeignKey(dish_category.DishCategory,
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    name = models.CharField(max_length=100, unique=True,
                            error_messages={'unique': ('A dish with such name '
                                                       'already exists.'), })
    photo = models.ImageField(upload_to='dish_images', blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    price = models.FloatField(default=0, null=False)
    weight = models.FloatField(default=0, null=False)
    available = models.BooleanField(default=True)

    class Meta():

        """Give some options attached to the model."""

        db_table = 'dishes'
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
