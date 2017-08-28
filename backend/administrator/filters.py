"""Encapsulate the logic for displaying filters in the Django admin."""
from django.contrib.admin.filters import ChoicesFieldListFilter


class ChoiceDropdownFilter(ChoicesFieldListFilter):

    """Implement dropdown filter."""

    template = 'admin/dropdown_filter.html'
