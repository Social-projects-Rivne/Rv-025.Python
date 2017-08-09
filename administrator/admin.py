from __future__ import unicode_literals

from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from .filters import ChoiceDropdownFilter
from administrator.models import DishCategory
from administrator.models import User
from restaurant.models import Dish
from restaurant.models import Restaurant


class RegistrationForm(UserCreationForm):

    """A form for users creation.

    Email, name, password and role are given.
    """

    email = forms.EmailField(required=True)

    class Meta:

        """Give some options (metadata) attached to the form."""

        model = User
        fields = ("role",)

    def save(self, commit=True):
        """Save a new user.

        Return a User object.
        """
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data["role"]
        user.set_is_staff(user.role)
        user.save()
        user.set_permissions(user.role)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    """A form for users modification."""

    class Meta:

        """Give some options (metadata) attached to the form."""

        model = User
        fields = ("name", "email", "phone", "role", "status",)

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

    search_fields = ("name", "email", "phone")
    list_display = ("name", "email", "phone", "role", "status")
    ordering = ["name"]
    list_per_page = 10
    list_filter = [
        ("status", ChoiceDropdownFilter),
        ("role", ChoiceDropdownFilter)
    ]

    fieldsets = (
        (None, {"fields": ("name", "email",)}),
        (_("Personal info"), {"fields": ("phone",)}),
        (_("Status"), {"fields": ("status",)}),
        (_("Permissions"), {"fields": ("role",)}),
    )

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """Function, that shows only Manager and Sub-manager roles
        when Manager adds Sub-manager.
        """
        if db_field.name == "role":
            if request.user.role == User.ROLE_MANAGER:
                kwargs['choices'] = (
                    (User.ROLE_SUB_MANAGER, "Sub-manager"),
                )
        return super(UserAdmin, self).formfield_for_choice_field(
            db_field, request, **kwargs)

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            "fields": ("email", "name", "password1", "password2", "role")}
         ),
    )

    actions = [delete_selected_users]


def soft_delete(modeladmin, request, queryset):
    """Soft delete function for QuerySet list."""
    for obj in queryset:
        obj.delete()


soft_delete.short_description = "Delete selected items"


def clone(modeladmin, queryset):
    """Clone instance"""
    for object in queryset:
        object.id = None
        object.save()


clone.short_description = "Clone"


class RestaurantForm(forms.ModelForm):

    """A form for restaurants modifications."""

    class Meta:

        """Give some options (metadata) attached to the form."""

        model = Restaurant
        fields = ("name", "logo", "location", "restaurant_type",
                  "tables_count", "description", "status",
                  "manager", "parent_restaurant")

    def __init__(self, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        restaurants = Restaurant.objects.all()

        manager_choices = [(None, "---------")]

        for user in users:
            if (user.status != User.STATUS_DELETED and
                    user.role == User.ROLE_MANAGER):
                manager_choices.append((user.pk, user.get_full_name()))

        self.fields["manager"].choices = manager_choices

        parent_restaurant_choices = [(None, "---------")]

        if self.current_user.role != User.ROLE_ADMIN:
            for restaurant in restaurants:
                if (restaurant.status != User.STATUS_DELETED
                        and restaurant.manager_id == self.current_user.id):
                    parent_restaurant_choices.append(
                        (restaurant.id, restaurant.name)
                    )
        else:
            for restaurant in restaurants:
                parent_restaurant_choices.append(
                    (restaurant.id, restaurant.name)
                )

        self.fields["parent_restaurant"].choices = parent_restaurant_choices

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
        if request.user.role == User.ROLE_ADMIN:
            return qs
        return qs.filter(manager=request.user.id)

    def get_form(self, request, *args, **kwargs):
        """Return a ModelForm class with current user id for using in the
        admin"""
        form = super(RestaurantAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form

    form = RestaurantForm
    list_display = ("name", "restaurant_type", "status",
                    "tables_count", "manager")
    list_per_page = 15
    actions = [soft_delete, clone]
    admin.site.disable_action('delete_selected')
    list_filter = [('status', ChoiceDropdownFilter)]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """View for the model instance editing page."""
        extra_context = {
            "clone_url": request.path.replace("change/", "clone/")
        }

        return super(RestaurantAdmin, self).change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )

    def get_urls(self):
        """Return the URLs to be used for that ModelAdmin."""
        urls = super(RestaurantAdmin, self).get_urls()

        custom_urls = [
            url(
                r'^(?P<restaurant>.+)/clone/$',
                self.admin_site.admin_view(self.clone_view),
                name='clone',
            )
        ]

        return custom_urls + urls

    def clone_view(self, request, *args, **kwargs):
        """View for cloning instance."""
        new_restaurant = Restaurant.objects.get(id=kwargs["restaurant"])
        new_restaurant.id = None
        new_restaurant.save()

        return HttpResponseRedirect("/admin/restaurant/restaurant/")

    def _type_id(self, obj):
        return obj.type_id
    _type_id.short_description = "restaurant type"


class DishCategoryAdmin(admin.ModelAdmin):

    """Custom display dishes categories list."""

    list_display = ("name", "id", "is_visible")
    list_per_page = 20
    ordering = ["name"]

    def has_add_permission(self, request):
        return request.user.role == User.ROLE_ADMIN

    def has_change_permission(self, request, obj=None):
        return request.user.role == User.ROLE_ADMIN

    def has_delete_permission(self, request, obj=None):
        return request.user.role == User.ROLE_ADMIN


class DishAdmin(admin.ModelAdmin):

    """Custom display dishes list."""

    list_display = ("name", "category", "price", "weight", "available")
    ordering = ["name"]

    def has_add_permission(self, request):
        return (request.user.role == User.ROLE_ADMIN or
                request.user.role == User.ROLE_MANAGER)

    def has_change_permission(self, request, obj=None):
        return (request.user.role == User.ROLE_ADMIN or
                request.user.role == User.ROLE_MANAGER)

    def has_delete_permission(self, request, obj=None):
        return (request.user.role == User.ROLE_ADMIN or
                request.user.role == User.ROLE_MANAGER)


admin.site.register(User, UserAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(DishCategory, DishCategoryAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.unregister(Group)
