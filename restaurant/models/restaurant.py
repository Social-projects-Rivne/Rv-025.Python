from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from django.db import models

from administrator.models import User


class RestaurantType(models.Model):

    """Create table with types of Restaurants."""

    rest_type = models.CharField(max_length=256, blank=False)
    is_deleted = models.BooleanField(default=False)

    class Meta(object):

        """Correct display of restaurant type in restaurant's list."""

        verbose_name = u"Restaurant type"

        permissions = (
             ('read_restaurant', 'Can read information about restaurant'),
         )

    rest_type = models.CharField(max_length=256, blank=False)

    def __unicode__(self):
        return u"%s" % (self.rest_type)


class Restaurant(models.Model):

    """Model of restaurant object, creates from admin panel."""

    ACTIVE = 0
    DELETED = 1
    HIDDEN = 2

    RESTAURANT_STATUSES = (
        (ACTIVE, 'active'),
        (DELETED, 'deleted'),
        (HIDDEN, 'hidden'),
    )

    name = models.CharField(max_length=256, blank=False)
    logo = models.CharField(max_length=256, default="Logo_added")
    location = models.CharField(max_length=256, blank=False)
    type_id = models.ForeignKey(RestaurantType, blank=True, null=True)
    status = models.IntegerField(choices=RESTAURANT_STATUSES, default=0)
    tables_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    description = models.TextField(max_length=256)
    # owner_id = models.ForeignKey(User)

    class Meta(object):

        """Display correct field in restaurant's list."""

        verbose_name = u"Restaurant"

        permissions = (
             ('read_restaurant', 'Can read information about restaurant'),
         )

    name = models.CharField(max_length=256, blank=False)

    def __unicode__(self):
        """Display custom labels in restaurant's list"""
        return u"%s %s" % (self.type_id, self.name)

    def delete(self, *args, **kwargs):
        """Function for restaurant soft-deleting"""
        self.status = 1
        self.save()
