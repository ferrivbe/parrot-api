"""
File name: api_validations.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from utils.configurations.constants import ExceptionConstants, GenericConstants
from utils.exceptions.api_exceptions import (
    ForbiddenEntityException,
    InternalServerErrorException,
)


class ApiValidations:
    """
    The API validations class.
    """

    def __init__(self):
        """
        Creates a new instance of class ApiValidations.
        """
        pass

    def is_null(self, entity):
        """
        Validates if entity is None, if it is returns a HTTP code 500.

        :param object entity: The entity to evaluate.
        """
        if entity is None:
            raise InternalServerErrorException()

    def is_null_or_empty_string(self, string):
        """
        Validates if string is None or empty, if it is returns a HTTP code 500.

        :param string string: The string to evaluate.
        """
        if (string is None) or (string == GenericConstants.EMPTY_CHAR):
            raise InternalServerErrorException()

    def is_role_valid(self, role, expected_role):
        """
        Validates if role can perform action.
        :param int role: The user role.
        :param int expected_role: The role needed to perform action.
        """
        if role != expected_role:
            raise ForbiddenEntityException(
                ExceptionConstants.USER_ROLE_NOT_VALID % {GenericConstants.ROLE: role}
            )
