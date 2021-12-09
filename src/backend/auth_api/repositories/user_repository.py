"""
File name: user_repository.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from django.contrib.auth.models import update_last_login
from django.utils import timezone

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from auth_api.models import User
from utils.configurations.constants import ExceptionConstants, GenericConstants
from utils.exceptions.api_exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)
from utils.validations.api_validations import ApiValidations


class UserRepository:
    """
    The user repository.

    Handles transactions between services and repositories.
    """

    def __init__(self):
        """
        Creates a new instance of UserRepository.
        """
        self.validator = ApiValidations()
        pass

    def create_user(self, user):
        """
        Creates a user.

        :param UserRegisterSerializer user: The user.
        """
        self.validator.is_null(user)

        self.__validate_entity_not_exists(user.validated_data)
        user.save()

        return self.__get_user_by_credentials_email(
            user.validated_data.get(GenericConstants.EMAIL)
        )

    def get_user(self, id):
        """
        Gets a user.

        :param uuid id: The user identifier.
        """
        self.validator.is_null(id)

        user = self.__get_user(id)
        return user

    def get_user_by_email(self, email):
        """
        Gets a user by email.

        :param string email: The user email.
        """
        self.validator.is_null_or_empty_string(email)

        user = self.__get_user_by_credentials_email(email)
        return user

    def delete_user(self, id):
        """
        Deeltes a user.

        :param uuid id: The user identifier.
        """
        self.validator.is_null(id)

        user = self.__get_user(id)
        user.is_active = False
        user.deleted_at = timezone.now()
        user.save()

        return user

    def update_password(self, user_data, id):
        """
        Updates a user password.

        :param UserPasswordSerializer user_data: The user data.
        :param uuid id: The user identifier.
        """
        self.validator.is_null(user_data)
        self.validator.is_null(id)

        user = self.__get_user(id)
        user.updated_at = timezone.now()
        user.set_password(user_data.validated_data.get(GenericConstants.PASSWORD))
        user.save()

        return user

    def validate_user(self, user):
        """
        Validates users for log-in

        :param User user: The user to validate.
        """
        self.validator.is_null(user)

        access_token_data = AccessToken.for_user(user)
        refresh_token = str(RefreshToken.for_user(user))
        access_token = str(AccessToken.for_user(user))
        expires_in = int(access_token_data.lifetime.total_seconds())

        update_last_login(None, user)

        validation = {
            GenericConstants.ACCESS_TOKEN: access_token,
            GenericConstants.REFRESH_TOKEN: refresh_token,
            GenericConstants.EXPIRES_IN: expires_in,
            GenericConstants.EMAIL: user.email,
            GenericConstants.ROLE: user.role,
        }

        return validation

    def __get_user(self, id):
        """
        Gets a user.

        :param uuid id: The user identifier.
        """
        self.validator.is_null(id)

        users = User.objects.filter(id=id, deleted_at=None)
        if users.count() < 1:
            raise NotFoundException(
                ExceptionConstants.USER_BY_ID_NOT_FOUND % {GenericConstants.ID: id}
            )

        return users.first()

    def __get_user_by_credentials_email(self, email):
        """
        Gets user by credentials.

        :param string email: The user email.
        """
        self.validator.is_null_or_empty_string(email)

        users = User.objects.filter(email=email, deleted_at=None)
        if users.count() < 1:
            raise NotFoundException(
                ExceptionConstants.USER_BY_EMAIL_NOT_FOUND
                % {GenericConstants.EMAIL: email}
            )

        return users.first()

    def __validate_entity_not_exists(self, user_data):
        """
        Validates whether entity exists.

        :param dict user_data: The user data.
        """
        self.validator.is_null(user_data)

        user_errors = []

        if (
            User.objects.filter(
                email=user_data.get(GenericConstants.EMAIL), deleted_at=None
            ).count()
            > 0
        ):
            user_errors.append(ExceptionConstants.EMAIL_ALREADY_EXISTS)

        first_name = user_data.get(GenericConstants.FIRST_NAME)
        last_name = user_data.get(GenericConstants.LAST_NAME)

        if (
            User.objects.filter(
                first_name__iexact=first_name,
                last_name__iexact=last_name,
                deleted_at=None,
            ).count()
            > 0
        ):
            user_errors.append(
                ExceptionConstants.NAME_ALREADY_IN_USE
                % {
                    GenericConstants.NAME: (
                        first_name + GenericConstants.SPACE + last_name
                    )
                }
            )

        if len(user_errors) > 0:
            raise UnprocessableEntityException(
                GenericConstants.LINE_BREAK.join(user_errors)
            )
