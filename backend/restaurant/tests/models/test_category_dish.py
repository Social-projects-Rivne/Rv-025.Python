"""Test DishCategory model."""

from django.test import TestCase

from restaurant.models import DishCategory


class DishCategoryTestCase(TestCase):

    """Test DishCategory model."""

    def setUp(self):
        """Prepare the test fixture."""

        self.dish_category = DishCategory()
        self.dish_category.name = "juice"
        self.dish_category.is_visible = True

    def test_create_dish_category(self):
        """Test if dish category is instance of DishCategory."""
        assert isinstance(self.dish_category, DishCategory)
