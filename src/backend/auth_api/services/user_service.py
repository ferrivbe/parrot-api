"""
File name: user_service.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from django.contrib.auth import authenticate

from auth_api.repositories.user_repository import UserRepository
from auth_api.serializers import user_authenticated, user_list
from utils.configurations.constants import GenericConstants
from utils.validations.api_validations import ApiValidations


class UserService:
    """
    The user service.

    Handles transactions between request and repository.
    """

    def __init__(self):
        """
        Creates a new instance of UserService.
        """
        self.auth_serializer = user_authenticated.UserAuthenticatedSerializer
        self.serializer = user_list.UserListSerializer
        self.user_repository = UserRepository()
        self.validator = ApiValidations()

    def create_user(self, user):
        """
        Creates a user.

        :param UserRegisterSerializer user: The user.
        """
        self.validator.is_null(user)

        user_created = self.user_repository.create_user(user)

        return self.__create_user_response(user_created).data

    def delete_user(self, id):
        """
        Deletes a user fully.

        :param uuid id: The user identifier.
        """
        self.validator.is_null(id)

        user = self.user_repository.delete_user(id)

        return self.__create_user_response(user).data

    def get_user(self, id):
        """
        Gets a user.

        :param uuid id: The user identifier.
        """
        self.validator.is_null(id)

        user = self.user_repository.get_user(id)

        return self.__create_user_response(user).data

    def update_password(self, user_data, id):
        """
        Updates a user password.

        :param UserPasswordSerializer user_data: The user data.
        :param uuid id: The user identifier.
        """
        self.validator.is_null(user_data)
        self.validator.is_null(id)

        user = self.user_repository.update_password(user_data, id)

        return self.__create_user_response(user).data

    def validate_user(self, user):
        """
        Validates user login data.
        """
        self.validator.is_null(user)

        email = user.data.get(GenericConstants.EMAIL)
        password = user.data.get(GenericConstants.PASSWORD)

        user = self.user_repository.get_user_by_email(email)

        user_authenticated = authenticate(email=email, password=password)
        user_validated = self.user_repository.validate_user(user_authenticated)

        return self.auth_serializer(user_validated).data

    def __create_user_response(self, user):
        """
        Creates a user response.

        :param User user: The user.
        """
        self.validator.is_null(user)

        return self.serializer(user)
