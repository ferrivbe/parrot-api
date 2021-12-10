"""
File name: test_user_manager.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework.test import APITestCase

from auth_api.models import User
from utils.exceptions.api_exceptions import (
    InternalServerErrorException,
    UnprocessableEntityException,
)


class UserManagerTestCase(APITestCase):
    """
    The user manager test class.
    """

    def test_create_user(self):
        """
        Tests the create_user method in user manager.

        Should return user when data is correct.
        """
        # arrange
        email = "test@test.com"

        # act
        User.objects.create_user(
            email=email,
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=1,
        )

        user = User.objects.get(email=email)

        # assert
        self.assertEqual(email, user.email)

    def test_create_user_internal_server_error_email(self):
        """
        Tests the create_user method in user manager.

        Should raise internal server error when email is None or empty string.
        """
        # arrange
        email = ""
        password = "test"
        role = 2

        # act

        # assert
        self.assertRaises(
            InternalServerErrorException,
            User.objects.create_user,
            email=email,
            password=password,
            role=role,
        )

    def test_create_user_internal_server_error_password(self):
        """
        Tests the create_user method in user manager.

        Should raise internal server error when email is None or empty string.
        """
        # arrange
        email = "test@test.com"
        password = ""
        role = 2

        # act

        # assert
        self.assertRaises(
            InternalServerErrorException,
            User.objects.create_user,
            email=email,
            password=password,
            role=role,
        )

    def test_create_superuser(self):
        """
        Tests the create_superuser method in user manager.

        Should return superuser when data is correct.
        """
        # arrange
        email = "test@test.com"

        # act
        User.objects.create_superuser(
            email=email,
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=1,
        )

        superuser = User.objects.get(email=email)

        # assert
        self.assertEqual(email, superuser.email)

    def test_create_superuser_unprocessable_entity(self):
        """
        Tests the create_superuser method in user manager.

        Should raise unprocessable entity exception when role is incorrect.
        """
        # arrange
        email = "test@test.com"
        password = "test"
        role = 2

        # act

        # assert
        self.assertRaises(
            UnprocessableEntityException,
            User.objects.create_superuser,
            email=email,
            password=password,
            role=role,
        )
