# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin

from .models import User


class UserCreationForm(forms.ModelForm):
    """Сreate new users.

    Include all the required fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        """Check that the two password entries match"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Save the provided password in hashed format and put
        is_active into appropriate value (according to the
        user's status)
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.set_is_active('status')
        if commit:
            user.save()
        return user


class UserAdmin(Admin):
    """Represent a model in the admin interface."""

    # The form to add user instances
    add_form = UserCreationForm

    # fields = ['username', 'email', 'password', 'phone', 'is_staff']
    list_display = ('username', 'email', 'phone', 'status', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'phone')}),
        ('Status', {'fields': ('status',)}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password1', 'password2', 'status')}
        ),
    )

# Register your models.
admin.site.register(User, UserAdmin)
