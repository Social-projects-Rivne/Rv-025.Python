"""
Allow to add category of dishes in database.
Contain a model class for dish category.
"""

from django.db import models


class DishCategory(models.Model):

    """Model of dish categories, creates from admin panel."""

    name = models.CharField(max_length=256, blank=False)
    is_visible = models.BooleanField(default=True, blank=True)

    class Meta(object):

        """Display correct field in dish_categories table."""

        db_table = 'dish_category'
        verbose_name_plural = u"Dish Categories"
        permissions = (
             ('read_dishcategory', 'Can read Dish Categories'),
        )

    def __str__(self):
        return self.name
