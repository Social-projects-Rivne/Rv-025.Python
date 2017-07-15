# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):
    """Represent a model in the admin interface."""
    fields = ['username', 'email', 'password', 'phone', 'is_staff']

# Register your models.
admin.site.register(User, UserAdmin)
