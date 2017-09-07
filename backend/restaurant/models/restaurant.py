"""
Allow to create a restaurant in a database.
Contain a model classes for restaurant and restaurant type.
:copyright: (c) 2017 by Serhii Kryzhanovskyi
"""

from django.core.validators import MinValueValidator

from django.db import models

from administrator.models import User


class RestaurantType(models.Model):

    """Restaurants type model."""

    restaurant_type = models.CharField(max_length=256, blank=False)
    is_deleted = models.BooleanField(default=False)

    class Meta(object):

        """Correct display of restaurant type in restaurant's list."""

        verbose_name_plural = u"Restaurant Type"

        permissions = (
            ("read_restauranttype",
             "Can read information about restaurant type"),
        )

    def __unicode__(self):
        return u"%s" % (self.restaurant_type, )


class Restaurant(models.Model):

    """Model of restaurant object, creates from admin panel."""

    STATUS_ACTIVE = 0
    STATUS_DELETED = 1
    STATUS_HIDDEN = 2

    RESTAURANT_STATUSES = (
        (STATUS_ACTIVE, "active"),
        (STATUS_DELETED, "deleted"),
        (STATUS_HIDDEN, "hidden"),
    )

    name = models.CharField(max_length=256, blank=False)
    logo = models.CharField(max_length=256, default="Logo_added")
    location = models.CharField(max_length=256, blank=False)
    phone = models.CharField(max_length=256, blank=False)
    restaurant_type = models.ForeignKey(RestaurantType, blank=True, null=True)
    status = models.IntegerField(choices=RESTAURANT_STATUSES, default=0)
    tables_count = models.IntegerField(default=0,
                                       validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    manager = models.ForeignKey(User, null=True, blank=True,
                                related_name='manager')
    sub_manager = models.ForeignKey(User, null=True, blank=True,
                                    related_name='sub_manager')

    class Meta(object):

        """Display correct field in restaurant's list."""

        verbose_name = u"Restaurant"

        permissions = (
            ("read_restaurant", "Can read information about restaurant"),
        )

    def __unicode__(self):
        """Display custom labels in restaurant's list"""
        return u"%s %s" % (self.restaurant_type, self.name)

    def delete(self, *args, **kwargs):
        """Function for restaurant soft-deleting"""
        self.status = Restaurant.STATUS_DELETED
        self.save()

    def set_manager(self, user):
        """Set manager to a restaurant."""
        if user.role == User.ROLE_ADMIN:
            if not User.last_active_admin(user):
                role = User.ROLE_MANAGER
            else:
                role = User.ROLE_ADMIN
        else:
            role = User.ROLE_MANAGER
        user.role = role
        user.set_permissions(role)
        user.set_is_staff(role)
        user.save()

    def set_sub_manager(self, user):
        """Set manager to a restaurant."""
        if user.role == User.ROLE_ADMIN:
            if not User.last_active_admin(user):
                role = User.ROLE_SUB_MANAGER
            else:
                role = User.ROLE_ADMIN
        elif user.role == User.ROLE_MANAGER:
            role = user.role
        else:
            role = User.ROLE_SUB_MANAGER
        user.role = role
        user.set_permissions(role)
        user.set_is_staff(role)
        user.save()
