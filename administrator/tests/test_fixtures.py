from django.test import TestCase

from administrator.models import Role

class FixturesTestCase(TestCase):

    fixtures = ['roles.json',]

    def test_fixtures_ammount(self):
        """Check if initial data can be loaded correctly"""
        self.assertEqual(Role.objects.all().count(), 4)