"""Test UserManager class and User model."""

from django.test import TestCase

from administrator.models import User, UserManager


class UserManagerTestCase(TestCase):

    """Test UserManager class."""

    valid_email = 'example@example.com'
    valid_username = 'foobar'
    valid_password = 'aprjvnsotmv890326sdH'

    def setUp(self):
        """Prepare the test fixture."""
        self.user_manager = UserManager()
        self.user_manager.model = User

    def test_user_is_not_created_without_email(self):
        """Test if user is not created without email."""
        with self.assertRaises(ValueError):
            self.user_manager.create_user('', '', '')

    def test_user_is_not_created_without_at_symbol_in_email(self):
        """Test if user is not created without @ in email."""
        wrong_email = "example"

        with self.assertRaises(ValueError):
            self.user_manager.create_user(
                wrong_email,
                self.valid_username,
                self.valid_password
            )

    def test_user_is_not_created_with_not_only_numbers_in_phone(self):
        """Test if user is not created with not only numeric phone."""
        wrong_phone = "0234hfk^&"

        with self.assertRaises(ValueError):
            self.user_manager.create_user(
                self.valid_email,
                self.valid_username,
                self.valid_password,
                phone=wrong_phone
            )

    def test_user_is_not_created_with_password_similar_to_personal_information(self):
        """Test if user is not created with password similar to personal information."""
        valid_email = 'example@example.com'
        wrong_password = "example"

        with self.assertRaises(ValueError):
            self.user_manager.create_user(
                valid_email,
                self.valid_username,
                wrong_password
            )

    def test_user_is_not_created_with_too_short_password(self):
        """Test if user is not created with too short password."""
        wrong_password = "qwerty1"

        with self.assertRaises(ValueError):
            self.user_manager.create_user(
                self.valid_email,
                self.valid_username,
                wrong_password
            )

    def test_user_is_not_created_with_only_numeric_password(self):
        """Test if user is not created with only numeric password."""
        wrong_password = "123456789"

        with self.assertRaises(ValueError):
            self.user_manager.create_user(
                self.valid_email,
                self.valid_username,
                wrong_password
            )

    def test_user_is_not_created_with_commonly_used_password(self):
        """Test if user is not created with commonly used password."""
        wrong_password = "password"

        with self.assertRaises(ValueError):
            self.user_manager.create_user(
                self.valid_email,
                self.valid_username,
                wrong_password
            )

    def test_user_is_created(self):
        """Test if user is created with valid data."""
        user = self.user_manager.create_user(
            self.valid_email,
            self.valid_username,
            self.valid_password
        )
        self.assertEqual(user.is_superuser, False)

    def test_superuser_is_not_created_with_is_superuser_field_set_to_false(self):
        """Test if superuser is not created with is_superuser field set to false."""
        with self.assertRaises(ValueError):
            self.user_manager.create_superuser(
                self.valid_email,
                self.valid_username,
                self.valid_password,
                is_superuser=False
            )

    def test_superuser_is_created(self):
        """Test if superuser is created with valid data."""
        superuser = self.user_manager.create_superuser(
            self.valid_email,
            self.valid_username,
            self.valid_password
        )
        self.assertEqual(superuser.is_superuser, True)


class UserTestCase(TestCase):

    """Test User model."""

    def setUp(self):
        """Prepare the test fixture."""
        valid_email = 'example@example.com'

        self.user = User()
        self.user.email = valid_email

    def test_user_status_can_be_set_to_active(self):
        """Test if user status can be set to active."""
        self.user.set_is_active(0)
        self.assertEqual(self.user.is_active, True)

    def test_user_status_can_be_set_to_inactive(self):
        """Test if user status can be set to inactive."""
        self.user.set_is_active(1)
        self.assertEqual(self.user.is_active, False)

    def test_user_can_be_set_to_admin(self):
        """Test if user can be set to admin."""
        self.user.set_is_staff(1)
        self.assertEqual(self.user.is_staff, True)

    def test_user_cannot_be_set_to_admin(self):
        """Test if user cannot be set to admin."""
        self.user.set_is_staff(0)
        self.assertEqual(self.user.is_staff, False)

    def test_user_has_email_as_his_short_name(self):
        """Test if user has email as his short name."""
        short_name = self.user.get_short_name()
        self.assertEqual(short_name, self.user.email)
