# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from restaurant.models import Restaurant


def soft_delete(modeladmin, request, queryset):
    """Soft delete function for QuerySet list."""
    for obj in queryset:
        obj.delete()
soft_delete.short_description = "Delete selected items"

class PageAdmin(admin.ModelAdmin):

    """Custom display in restaurant's list."""

    list_display = ('name', '_type_id', 'status', 'tables_count')
    list_per_page = 15
    actions = [soft_delete]
    admin.site.disable_action('delete_selected')

    def _type_id(self, obj):
        return obj.type_id
    _type_id.short_description = 'restaurant type'

admin.site.register(Restaurant, PageAdmin)
