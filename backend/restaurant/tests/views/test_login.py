"""Test login view"""

from django.test import TestCase, Client

from administrator.models import User


class LogInTest(TestCase):

    """Test login view."""

    def setUp(self):
        self.client = Client()
        self.users_credentials = {
            "correct_user": {
                'email': 'valid@email.com',
                'password': 'gfhjkm12',
                'name': 'CorrectUser',
                'status': User.STATUS_ACTIVE,
                'role': User.ROLE_USER,
            },
            "banned_user": {
                'email': 'banned@email.com',
                'password': 'gfhjkm12',
                'username': 'BannedUser',
                'status': User.STATUS_BANNED,
                'role': User.ROLE_USER,
            },
            "unregistered_user": {
                'email': 'unregistered@email.com',
                'password': 'gfhjkm12',
            }}
        User.objects.create_user(**self.users_credentials["correct_user"])
        User.objects.create_user(**self.users_credentials["banned_user"])

    def test_login_correct_user(self):
        """Test whether user can login with correct data."""
        response = self.client.post('/accounts/login/',
                                    self.users_credentials["correct_user"],
                                    follow=True)
        self.assertContains(response, "Logout")

    def test_login_banned_user(self):
        """Test whether banned user can't login."""
        context = ("To proceed, please login with an account "
                   "that has access.")
        response = self.client.post('/accounts/login/',
                                    self.users_credentials["banned_user"],
                                    follow=True)
        self.assertContains(response, context)

    def test_login_unregistered_user(self):
        """Test whether user that isn't in database can't login."""
        context = "Please try again."
        response = self.client.post(
            '/accounts/login/',
            self.users_credentials["unregistered_user"],
            follow=True
        )
        self.assertContains(response, context)
