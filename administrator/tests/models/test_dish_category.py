"""Test DishCategory model."""

from django.test import TestCase

from administrator.models import DishCategory


class DishCategoryTestCase(TestCase):

    """Test DishCategory model."""

    def setUp(self):
        """Prepare the test fixture."""
        name = "juice"

        self.dish_category = DishCategory()
        self.dish_category.name = name

    def test_dish_category_is_not_created_without_name(self):
        """Test if dish category is not created without name."""
        with self.assertRaises(ValueError):
            self.dish_category._save("")

    def test_dish_category_can_be_set_to_deleted(self):
        """Test if dish category can be set to deleted."""
        self.dish_category.delete()
        self.assertEqual(self.dish_category.is_delete, True)
