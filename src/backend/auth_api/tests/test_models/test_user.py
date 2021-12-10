"""
File name: test_user.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from django.test import TestCase

from auth_api.models import User


class UserTestCase(TestCase):
    """
    The user model testing class.
    """

    def test_user(self):
        """
        Tests the user model.

        Should return email when called.
        """
        # arrange
        expected_email = "test@test.com"

        # act
        user = User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=1,
        )

        # assert
        self.assertEqual(expected_email, user.__str__())
