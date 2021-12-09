"""
File name: managers.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from django.contrib.auth.base_user import BaseUserManager

from utils.configurations.constants import ExceptionConstants, GenericConstants
from utils.exceptions.api_exceptions import UnprocessableEntityException
from utils.validations.api_validations import ApiValidations


class CustomUserManager(BaseUserManager):
    """
    Custom user model where the email address is the unique identifier
    and has an is_admin field to allow access to the admin app.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Creates a user.
        """
        self.manager = ApiValidations()
        self.manager.is_null_or_empty_string(email)
        self.manager.is_null_or_empty_string(password)

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates a superuser.
        """
        extra_fields.setdefault(GenericConstants.IS_ACTIVE, True)
        extra_fields.setdefault(GenericConstants.ROLE, 1)

        if extra_fields.get(GenericConstants.ROLE) != 1:
            raise UnprocessableEntityException(
                ExceptionConstants.SUPER_USER_ROLE_INVALID
            )
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        """
        Gets user by natural key.

        This method adds the 'deleted:at: None' filter for soft deleted
        records in database.
        """
        return self.get(
            **{self.model.USERNAME_FIELD: email, GenericConstants.DELETED_AT: None}
        )
