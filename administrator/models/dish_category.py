# -*- coding: utf-8 -*-
"""
Allow to add category of dishes in database.
Contain a model class for dish category.
"""

from django.db import models


class DishCategory(models.Model):

    """Model of dish categories, creates from admin panel."""

    # id = models.ForeignKey(Dish, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=False)
    is_delete = models.BooleanField(default=False, blank=True)

    class Meta(object):

        """Display correct field in dish_categories table."""

        db_table = 'dish_category'
        verbose_name = u"Dish Categories"
        permissions = (
             ('read_dishcategory', 'Can read information about Dish Categories'),
         )

    def _save(self, name, **extra_fields):
        """Create and save dish_categories with the given name."""
        return self._save(name, **extra_fields)

    def delete(self, *args, **kwargs):
        """Soft-deleting category"""
        self.is_delete = True
        self.save()
