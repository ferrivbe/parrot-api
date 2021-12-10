"""
File name: test_urls.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from django.test import SimpleTestCase
from django.urls import resolve, reverse

from auth_api.views.user_view import UserLoginView, UserView


class TestUrls(SimpleTestCase):
    """
    The urls test class.
    """

    def test_user_login_view(self):
        """
        Test users login url.
        """
        url = reverse("users-login")
        self.assertEqual(resolve(url).func.view_class, UserLoginView)

    def test_user_view(self):
        """
        Test users url.
        """
        url = reverse("users")
        self.assertEqual(resolve(url).func.view_class, UserView)
