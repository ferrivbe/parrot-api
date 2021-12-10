"""
File name: test_apps.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from django.apps import apps
from django.test import TestCase

from auth_api.apps import AuthApiConfig


class AuthApiConfigTestCase(TestCase):
    """
    The auth_api apps testing class.
    """

    def test_apps(self):
        """
        Tests the auth_api app apps.py file
        """
        self.assertEqual(AuthApiConfig.name, "auth_api")
        self.assertEqual(apps.get_app_config("auth_api").name, "auth_api")
