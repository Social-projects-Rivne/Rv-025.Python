# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .filters import ChoiceDropdownFilter
from .models import DishCategory
from .models import Role
from .models import User
from restaurant.models import Restaurant


class RegistrationForm(UserCreationForm):

    """A form for users creation.

    Email, name, password and role are given.
    """

    email = forms.EmailField(required=True)

    class Meta:

        """Give some options (metadata) attached to the form."""

        model = User
        fields = ('role',)

    def save(self, commit=True):
        """Save a new user.

        Return a User object.
        """
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.set_is_staff(user.role)
        user.set_permissions(user.role)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    """A form for users modification."""

    class Meta:

        """Give some options (metadata) attached to the form."""

        model = User
        fields = ('name', 'email', 'phone', 'role', 'status',)

    def save(self, commit=True):
        """Save the provided password in a hashed format and put
        is_active into an appropriate value (according to the
        user's status)

        Return a User object.
        """
        user = super(UserChangeForm, self).save(commit=False)
        user.set_is_active(user.status)
        user.set_is_staff(user.role)
        user.set_permissions(user.role)
        if commit:
            user.save()
        return user


def delete_selected_users(modeladmin, request, queryset):
    """Block selected users instead of dropping them."""
    for obj in queryset:
        obj.delete()


delete_selected_users.short_description = "Delete selested users"


class UserAdmin(Admin):

    """Represent a model in the admin interface."""

    form = UserChangeForm
    add_form = RegistrationForm

    search_fields = ('name', 'email', 'phone')
    list_display = ('name', 'email', 'phone', 'role', 'status')
    ordering = ['name']
    list_per_page = 10
    list_filter = [('status', ChoiceDropdownFilter), ('role', ChoiceDropdownFilter)]

    fieldsets = (
        (None, {'fields': ('name', 'email',)}),
        (_('Personal info'), {'fields': ('phone',)}),
        (_('Status'), {'fields': ('status',)}),
        (_('Permissions'), {'fields': ('role',)}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'fields': ('email', 'name', 'password1', 'password2', 'role')}
         ),
    )

    actions = [delete_selected_users]


def soft_delete(modeladmin, request, queryset):
    """Soft delete function for QuerySet list."""
    for obj in queryset:
        obj.delete()


soft_delete.short_description = "Delete selected items"


class RestaurantForm(forms.ModelForm):

    """A form for restaurants modifications."""


    class Meta:

        """Give some options (metadata) attached to the form."""

        model = Restaurant
        fields = ('name', 'logo', 'location', 'type', 'tables_count',
                  'description', 'status', 'manager')

    def __init__(self, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['manager'].choices = [(user.pk, user.get_full_name())
                                          for user in users
                                          if user.status != 1 and user.role
                                          == Role.objects.get(id=2)]

    def save(self, commit=True):
        """Save the restaurant.

        Return a Restaurant object.
        """
        restaurant = super(RestaurantForm, self).save(commit=False)

        if restaurant.manager:
            restaurant.set_manager(restaurant.manager)

        if commit:
            restaurant.save()
        return restaurant


class RestaurantAdmin(admin.ModelAdmin):

    """Custom display in restaurant's list."""

    def get_queryset(self, request):
        """ Represent the objects.

        Return a QuerySet of all model instances that can be edited
        by the admin site.
        """
        qs = super(RestaurantAdmin, self).get_queryset(request)
        if request.user.role == Role.objects.get(id=1):
            return qs
        return qs.filter(manager=request.user.id)

    form = RestaurantForm

    list_display = ('name', 'type', 'status', 'tables_count', 'manager')
    list_per_page = 15
    actions = [soft_delete]
    admin.site.disable_action('delete_selected')
    list_filter = [('status', ChoiceDropdownFilter)]

    def _type_id(self, obj):
        return obj.type_id
    _type_id.short_description = 'restaurant type'


class DishCategoryAdmin(admin.ModelAdmin):

    """Custom display dishes categories list."""

    list_display = ('name', 'id', 'is_delete')
    list_per_page = 15


admin.site.register(User, UserAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(DishCategory, DishCategoryAdmin)
admin.site.unregister(Group)
