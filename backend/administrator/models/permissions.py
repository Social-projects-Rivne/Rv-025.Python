"""
Get permissions for different roles.
"""

from django.contrib.auth.models import Permission


def get_permission(codename):
    """Get permission from db by codename.

    Argument:
    codename (str) - codename of permission
    """
    return Permission.objects.get(codename=codename)


def admin_permissions():
    """Return list of admin's permissions."""
    admin_permissions = [
        "add_logentry",
        "change_logentry",
        "delete_logentry",
        "add_user",
        "change_user",
        "delete_user",
        "read_user",
        "add_group",
        "change_group",
        "delete_group",
        "add_permission",
        "change_permission",
        "delete_permission",
        "add_contenttype",
        "change_contenttype",
        "delete_contenttype",
        "add_restaurant",
        "change_restaurant",
        "delete_restaurant",
        "read_restaurant",
        "add_restauranttype",
        "change_restauranttype",
        "delete_restauranttype",
        "read_restauranttype",
        "add_session",
        "change_session",
        "delete_session",
        "add_booking",
        "change_booking",
        "delete_booking",
        "read_booking",
        "add_dishcategory",
        "change_dishcategory",
        "delete_dishcategory",
        "read_dishcategory",
    ]
    return [get_permission(item) for item in admin_permissions]


def manager_permissions():
    """Return list of manager's permissions."""
    manager_permissions = [
        "add_user",
        "change_user",
        "delete_user",
        "read_user",
        "add_restaurant",
        "change_restaurant",
        "delete_restaurant",
        "read_restaurant",
        "add_restauranttype",
        "change_restauranttype",
        "delete_restauranttype",
        "read_restauranttype",
        "change_booking",
        "read_booking",
    ]
    return [get_permission(item) for item in manager_permissions]


def sub_manager_permissions():
    """Return list of sub-manager's permissions."""
    sub_manager_permissions = [
        "read_user",
        "read_restaurant",
        "read_restauranttype",
        "change_booking",
        "read_booking",
    ]
    return [get_permission(item) for item in sub_manager_permissions]


def user_permissions():
    """Return list of user's permissions."""
    user_permissions = [
        "read_user",
        "read_restaurant",
    ]
    return [get_permission(item) for item in user_permissions]
