# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .models import User


class RegistrationForm(UserCreationForm):

    """A form for users creation.

    Email, username, password and role are given.
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
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    """A form for users modification."""

    class Meta:

        """Give some options (metadata) attached to the form."""

        model = User
        fields = ('username', 'email', 'phone', 'role', 'status',)

    def save(self, commit=True):
        """Save the provided password in a hashed format and put
        is_active into an appropriate value (according to the
        user's status)

        Return a User object.
        """
        user = super(UserChangeForm, self).save(commit=False)
        user.set_is_active(user.status)
        user.set_is_staff(user.role)
        if commit:
            user.save()
        return user


class UserAdmin(Admin):

    """Represent a model in the admin interface."""

    form = UserChangeForm
    add_form = RegistrationForm

    search_fields = ('username', 'email', 'phone')
    list_display = ('username', 'email', 'phone', 'role', 'status')
    ordering = ['username']
    list_per_page = 10

    fieldsets = (
        (None, {'fields': ('username', 'email',)}),
        (_('Personal info'), {'fields': ('phone',)}),
        (_('Status'), {'fields': ('status',)}),
        (_('Permissions'), {'fields': ('role', 'user_permissions')}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password1', 'password2', 'role')}
         ),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
