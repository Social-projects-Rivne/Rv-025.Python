from django.test import TestCase

from administrator.models import User, UserManager


class UserManagerTestCase(TestCase):
    valid_email = 'example@example.com'
    valid_username = 'foobar'
    valid_password = 'qwerty123'

    def setUp(self):
        self.user_manager = UserManager()
        self.user_manager.model = User

    def test_user_is_not_created_without_email(self):
        with self.assertRaises(ValueError):
            self.user_manager.create_user('', '', '')

    def test_user_is_created(self):
        user = self.user_manager.create_user(self.valid_email, self.valid_username, self.valid_password)
        self.assertEqual(user.is_superuser, False)

    def test_superuser_is_not_created_with_is_superuser_field_set_to_false(self):
        with self.assertRaises(ValueError):
            self.user_manager.create_superuser(self.valid_email, self.valid_username, self.valid_password,
                                               is_superuser=False)

    def test_superuser_is_created(self):
        superuser = self.user_manager.create_user(self.valid_email, self.valid_username, self.valid_password)
        self.assertEqual(superuser.is_superuser, True)


class UserTestCase(TestCase):
    valid_email = 'example@example.com'

    def setUp(self):
        self.user = User()
        self.user.email = self.valid_email

    def test_user_status_can_be_set_to_active(self):
        self.user.set_status_and_is_active(0)
        self.assertEqual(self.user.status, 0)
        self.assertEqual(self.user.is_active, True)

    def test_user_status_can_be_set_to_inactive(self):
        self.user.set_status_and_is_active(1)
        self.assertEqual(self.user.status, 1)
        self.assertEqual(self.user.is_active, False)

    def test_user_has_email_as_his_short_name(self):
        short_name = self.user.get_short_name()
        self.assertEqual(short_name, self.user.email)
