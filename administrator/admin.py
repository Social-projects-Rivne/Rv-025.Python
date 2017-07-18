# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin

from .filters import ChoiceDropdownFilter
from .models import User
from restaurant.models import Restaurant


class UserAdmin(Admin):

    """Represent a model in the admin interface."""

    list_display = ('username', 'email', 'phone', 'role', 'status')
    list_filter = [('status', ChoiceDropdownFilter), 'role']


class RestaurantAdmin(admin):

    """Represent a Restaurant model in the admin interface."""

    list_filter = ['status', ('owner_id', ChoiceDropdownFilter)]

admin.site.register(User, UserAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
