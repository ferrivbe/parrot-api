"""
File name: test_user_view.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from django.utils import timezone
from rest_framework.test import APITestCase

from rest_framework_simplejwt.tokens import AccessToken

from auth_api.models import User
from utils.exceptions.api_exceptions import (
    BadRequestException,
    ForbiddenEntityException,
    NotFoundException,
    UnauthorizedException,
    UnprocessableEntityException,
)


class UserTestCase(APITestCase):
    """
    The user view test case class.
    """

    def test_user_get(self):
        """
        Tests the GET method of UserView.

        Should return HTTP status 200 when authentication provided.
        """
        # arrange
        user = User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=1,
        )

        token = str(AccessToken.for_user(user=user))

        expected = {
            "first_name": "test_name",
            "last_name": "test_last_name",
            "email": "test@test.com",
            "role": 1,
        }

        # act
        self.client.force_authenticate(user=user)
        response = self.client.get(
            "/users", None, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, response.data)

    def test_user_get_not_found_when_soft_delete(self):
        """
        Tests the GET method of UserView.

        Should return HTTP status 404 when authentication provided but user not found.
        """
        # arrange
        user = User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=1,
        )

        token = str(AccessToken.for_user(user=user))

        instance = User.objects.get(email="test@test.com")
        instance.deleted_at = timezone.now()
        instance.is_active = False
        instance.save()

        # act
        self.client.force_authenticate(user=user)
        response = self.client.get(
            "/users", None, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 404)
        self.assertRaises(NotFoundException)

    def test_user_get_not_found_when_hard_delete(self):
        """
        Tests the GET method of UserView.

        Should return HTTP status 404 when authentication provided but user not found.
        """
        # arrange
        user = User.objects.create_superuser(
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=1,
        )

        token = str(AccessToken.for_user(user=user))

        instance = User.objects.get(email="test@test.com")
        instance.delete()

        # act
        self.client.force_authenticate(user=user)
        response = self.client.get(
            "/users", None, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 404)
        self.assertRaises(NotFoundException)

    def test_user_get_unauthorized(self):
        """
        Tests the GET method of UserView.

        Should return HTTP status 401 when authentication not provided.
        """
        # arrange

        # act
        response = self.client.get("/users", None)

        # assert
        self.assertEqual(response.status_code, 401)
        self.assertRaises(UnauthorizedException)

    def test_user_post(self):
        """
        Tests the POST method of UserView.

        Should return HTTP status 201 when data and authentication provided.
        """
        # arrange
        user_creator = User.objects.create_user(
            email="creator@creator.com",
            password="creator",
            first_name="creator_name",
            last_name="creator_last_name",
            role=1,
        )

        user_data = {
            "first_name": "test_name",
            "last_name": "test_last_name",
            "email": "test@test.com",
            "password": "test_password",
            "role": 2,
        }

        token = str(AccessToken.for_user(user=user_creator))

        expected = {
            "first_name": "test_name",
            "last_name": "test_last_name",
            "email": "test@test.com",
            "role": 2,
        }

        # act
        self.client.force_authenticate(user=user_creator)
        response = self.client.post(
            "/users", user_data, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(expected, response.data)

    def test_user_post_bad_request(self):
        """
        Tests the POST method of UserView.

        Should return HTTP status 422 when data and authentication provided
        but email already exists.
        """
        # arrange
        user_creator = User.objects.create_user(
            email="creator@creator.com",
            password="creator",
            first_name="creator_name",
            last_name="creator_last_name",
            role=1,
        )

        user_data = {
            "first_name": "test_name",
            "last_name": "test_last_name",
            "email": "test@test.com",
            "pass": "test_password",
            "role": 2,
        }

        token = str(AccessToken.for_user(user=user_creator))

        # act
        self.client.force_authenticate(user=user_creator)
        response = self.client.post(
            "/users", user_data, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 400)
        self.assertRaises(BadRequestException)

    def test_user_post_not_found(self):
        """
        Tests the POST method of UserView.

        Should return HTTP status 404 when data and authentication provided
        but email does not exist.
        """
        # arrange
        user_creator = User.objects.create_user(
            email="creator@creator.com",
            password="creator",
            first_name="creator_name",
            last_name="creator_last_name",
            role=1,
        )

        user_data = {
            "first_name": "test_name",
            "last_name": "test_last_name",
            "email": "test@test.com",
            "pass": "test_password",
            "role": 2,
        }

        token = str(AccessToken.for_user(user=user_creator))

        # act
        self.client.force_authenticate(user=user_creator)
        response = self.client.post(
            "/users", user_data, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 400)
        self.assertRaises(BadRequestException)

    def test_user_post_unprocessable_entity_name(self):
        """
        Tests the POST method of UserView.

        Should return HTTP status 422 when data and authentication provided
        but name already exists.
        """
        # arrange
        user_creator = User.objects.create_user(
            email="creator@creator.com",
            password="creator",
            first_name="creator_name",
            last_name="creator_last_name",
            role=1,
        )

        user_data = {
            "first_name": "creator_name",
            "last_name": "creator_last_name",
            "email": "test@test.com",
            "password": "test_password",
            "role": 2,
        }

        token = str(AccessToken.for_user(user=user_creator))

        # act
        self.client.force_authenticate(user=user_creator)
        response = self.client.post(
            "/users", user_data, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 422)
        self.assertRaises(UnprocessableEntityException)

    def test_user_post_unprocessable_entity_email(self):
        """
        Tests the POST method of UserView.

        Should return HTTP status 422 when data and authentication provided
        but email already exists.
        """
        # arrange
        user_creator = User.objects.create_user(
            email="creator@creator.com",
            password="creator",
            first_name="creator_name",
            last_name="creator_last_name",
            role=1,
        )

        user_data = {
            "first_name": "test_name",
            "last_name": "test_last_name",
            "email": "creator@creator.com",
            "password": "test_password",
            "role": 2,
        }

        token = str(AccessToken.for_user(user=user_creator))

        # act
        self.client.force_authenticate(user=user_creator)
        response = self.client.post(
            "/users", user_data, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 422)
        self.assertRaises(UnprocessableEntityException)

    def test_user_post_forbidden_same_role(self):
        """
        Tests the POST method of UserView.

        Should return HTTP status 403 when data and authentication provided but
        user tries to create other with same role.
        """
        # arrange
        user_creator = User.objects.create_user(
            email="creator@creator.com",
            password="creator",
            first_name="creator_name",
            last_name="creator_last_name",
            role=2,
        )

        user_data = {
            "first_name": "test_name",
            "last_name": "test_last_name",
            "email": "test@test.com",
            "password": "test_password",
            "role": 2,
        }

        token = str(AccessToken.for_user(user=user_creator))

        # act
        self.client.force_authenticate(user=user_creator)
        response = self.client.post(
            "/users", user_data, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 403)
        self.assertRaises(ForbiddenEntityException)

    def test_user_post_forbidden_higher_role(self):
        """
        Tests the POST method of UserView.

        Should return HTTP status 403 when data and authentication provided but
        user tries to create other with higher ranking role.
        """
        # arrange
        user_creator = User.objects.create_user(
            email="creator@creator.com",
            password="creator",
            first_name="creator_name",
            last_name="creator_last_name",
            role=2,
        )

        user_data = {
            "first_name": "test_name",
            "last_name": "test_last_name",
            "email": "test@test.com",
            "password": "test_password",
            "role": 1,
        }

        token = str(AccessToken.for_user(user=user_creator))

        # act
        self.client.force_authenticate(user=user_creator)
        response = self.client.post(
            "/users", user_data, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 403)
        self.assertRaises(ForbiddenEntityException)

    def test_user_post_unauthorized(self):
        """
        Tests the POST method of UserView.

        Should return HTTP status 401 when data is provided and authentication is not.
        """
        # arrange
        User.objects.create_user(
            email="creator@creator.com",
            password="creator",
            first_name="creator_name",
            last_name="creator_last_name",
            role=2,
        )

        user_data = {
            "first_name": "test_name",
            "last_name": "test_last_name",
            "email": "test@test.com",
            "password": "test_password",
            "role": 1,
        }

        # act
        response = self.client.post("/users", user_data)

        # assert
        self.assertEqual(response.status_code, 401)
        self.assertRaises(ForbiddenEntityException)

    def test_user_delete(self):
        """
        Tests the DELETE method of UserView.

        Should return HTTP status 200 and delete user when authentication provided.
        """
        # arrange
        user = User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=2,
        )

        token = str(AccessToken.for_user(user=user))

        expected = {
            "first_name": "test_name",
            "last_name": "test_last_name",
            "email": "test@test.com",
            "role": 2,
        }

        # act
        self.client.force_authenticate(user=user)
        response = self.client.delete(
            "/users", None, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, response.data)

    def test_user_delete_unauthorized_when_user_is_deleted(self):
        """
        Tests the DELETE method of UserView.

        Should return HTTP status 200 and delete user when authentication provided.
        Should return HTTP status 401 when deleted user authentication provided.
        """
        # arrange
        user = User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=2,
        )

        token = str(AccessToken.for_user(user=user))

        expected = {
            "first_name": "test_name",
            "last_name": "test_last_name",
            "email": "test@test.com",
            "role": 2,
        }

        # act
        response = self.client.delete(
            "/users", None, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )
        second_response = self.client.delete(
            "/users", None, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, response.data)
        self.assertEqual(second_response.status_code, 401)
        self.assertRaises(UnauthorizedException)

    def test_user_delete_not_found(self):
        """
        Tests the GET method of UserView.

        Should return HTTP status 404 when authentication provided but user not found.
        """
        # arrange
        user = User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=1,
        )

        token = str(AccessToken.for_user(user=user))

        instance = User.objects.get(email="test@test.com")
        instance.deleted_at = timezone.now()
        instance.is_active = False
        instance.save()

        # act
        self.client.force_authenticate(user=user)
        response = self.client.delete(
            "/users", None, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 404)
        self.assertRaises(NotFoundException)

    def test_user_patch(self):
        """
        Tests the PATCH method of UserView.

        Should return HTTP status 200 and update user password when password and
        authentication provided.
        """
        # arrange
        user_request = User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=2,
        )

        user_data = {"password": "new_test"}

        token = str(AccessToken.for_user(user=user_request))

        expected = {
            "first_name": "test_name",
            "last_name": "test_last_name",
            "email": "test@test.com",
            "role": 2,
        }

        # act
        self.client.force_authenticate(user=user_request)
        response = self.client.patch(
            "/users", user_data, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, response.data)

    def test_user_patch_bad_request(self):
        """
        Tests the PATCH method of UserView.

        Should return HTTP status 400 when data has erros and authentication provided.
        """
        # arrange
        user_request = User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=2,
        )

        user_data = {"pass": "new_test"}

        token = str(AccessToken.for_user(user=user_request))

        # act
        self.client.force_authenticate(user=user_request)
        response = self.client.patch(
            "/users", user_data, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 400)
        self.assertRaises(BadRequestException)

    def test_user_patch_not_found(self):
        """
        Tests the PATCH method of UserView.

        Should return HTTP status 404 when data and authentication provided but user not found.
        """
        # arrange
        user_request = User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=2,
        )

        user_data = {"password": "new_test"}

        token = str(AccessToken.for_user(user=user_request))

        instance = User.objects.get(email="test@test.com")
        instance.deleted_at = timezone.now()
        instance.is_active = False
        instance.save()

        # act
        self.client.force_authenticate(user=user_request)
        response = self.client.patch(
            "/users", user_data, **{"HTTP_AUTHORIZATION": "Bearer " + token}
        )

        # assert
        self.assertEqual(response.status_code, 404)
        self.assertRaises(NotFoundException)

    def test_user_patch_unauthorized(self):
        """
        Tests the PATCH method of UserView.

        Should return HTTP status 401 when data provided and authentication missing.
        """
        # arrange
        user_data = {"password": "new_test"}

        # act
        response = self.client.patch("/users", user_data)

        # assert
        self.assertEqual(response.status_code, 401)
        self.assertRaises(UnauthorizedException)
