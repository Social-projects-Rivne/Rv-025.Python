# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import User


class RegistrationForm(UserCreationForm):

    """A form for user creation.

    Email, username, password and role are given.
    """

    email = forms.EmailField(required=True)


    class Meta:

        """Give some options (metadata) attached to the form."""

        model = User
        fields = ('role',)


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.set_is_staff(user.role)
        if commit:
            user.save()
        return user


class UserAdmin(Admin):

    """Represent a model in the admin interface."""

    add_form = RegistrationForm

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password1', 'password2', 'role')}
         ),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
