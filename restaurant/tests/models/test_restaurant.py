"""Test UserManager class and User model."""

from django.test import TestCase

from restaurant.models import Restaurant


class RestaurantTestCase(TestCase):

    """Test Resaturant class."""

    def setUp(self):
        """Prepare the test fixture."""
        valid_name = "Tungalo"
        valid_location = "Rivne"
        valid_status = 0
        valid_tables_count = 10
        valid_description = "description"

        self.restaurant = Restaurant()
        self.restaurant.name = valid_name
        self.restaurant.location = valid_location
        self.restaurant.status = valid_status
        self.restaurant.tables_count = valid_tables_count
        self.restaurant.description = valid_description

    def test_restaurant_delete_satus_set_to_1(self):
        """Test if user status can be set to active."""
        self.restaurant.delete()
        self.assertEqual(self.restaurant.status, 1)
