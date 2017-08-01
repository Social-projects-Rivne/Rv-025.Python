"""Test DishCategory model."""

from django.test import TestCase

from administrator.models import DishCategory


class DishCategoryTestCase(TestCase):

    """Test DishCategory model."""

    def setUp(self):
        """Prepare the test fixture."""

        self.dish_category = DishCategory()
        self.dish_category.name = "juice"
        self.dish_category.is_delete = False

    def test_create_dish_category(self):
        """Test if dish category is instance of DishCategory."""
        assert isinstance(self.dish_category, DishCategory)

    def test_dish_category_can_be_set_to_deleted(self):
        """Test if dish category can be set to deleted."""
        self.dish_category.delete()
        self.assertEqual(self.dish_category.is_delete, True)
