"""
File name: test_user_login_view.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework.test import APITestCase

from auth_api.models import User
from utils.exceptions.api_exceptions import BadRequestException, NotFoundException


class UserLoginTestCase(APITestCase):
    """
    The user login view test case class.
    """

    def test_user_login_post(self):
        """
        Tests the POST method of UserLoginView.

        Should return HTTP status 200 when data provided and user found.
        """
        # arrange
        User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=1,
        )

        expected_email = "test@test.com"

        request_data = {"email": "test@test.com", "password": "test"}

        # act
        response = self.client.post("/users/login", request_data)

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_email, response.data.get("email"))

    def test_user_login_post_bad_request(self):
        """
        Tests the POST method of UserLoginView.

        Should return HTTP status 400 when data provided incorrectly.
        """
        # arrange
        User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=1,
        )

        request_data = {"email": "test@test.com", "pass": "test"}

        # act
        response = self.client.post("/users/login", request_data)

        # assert
        self.assertEqual(response.status_code, 400)
        self.assertRaises(BadRequestException)

    def test_user_login_post_not_found(self):
        """
        Tests the POST method of UserLoginView.

        Should return HTTP status 404 when data provided bu user not found.
        """
        # arrange
        request_data = {"email": "test@test.com", "password": "test"}

        # act
        response = self.client.post("/users/login", request_data)

        # assert
        self.assertEqual(response.status_code, 404)
        self.assertRaises(NotFoundException)
