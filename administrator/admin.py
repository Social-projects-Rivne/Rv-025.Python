# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from restaurant.models import Restaurant
# Register your models here.

def soft_delete(modeladmin, request, queryset):
    """Soft delete function for selected restaurants in list"""

    for obj in queryset:
        obj.delete()
soft_delete.short_description = "Delete selected items"

class PageAdmin(admin.ModelAdmin):
    #fields for restaurant list.
    list_display = ('name', '_type_id', 'status', 'tables_count')
    #restaurants per page.
    list_per_page = 15
    #overriding of Admin actions.
    actions = [soft_delete]
    admin.site.disable_action('delete_selected')

    def _type_id(self, obj):
        return obj.type_id
    _type_id.short_description = 'restaurant type'

admin.site.register(Restaurant, PageAdmin)
