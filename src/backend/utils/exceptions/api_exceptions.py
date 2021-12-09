"""
File name: api_exceptions.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    """
    The bad request exception resource.

    Status code: 400
    Detail: Bad request exception
    Code: bad_request_esception
    """

    status_code = 400
    default_detail = "Bad request exception"
    default_code = "bad_request_esception"


class UnauthorizedException(APIException):
    """
    The unauthorized exception resource.

    Status code: 401
    Detail: Unauthorized exception
    Code: unauthorized_exception
    """

    status_code = 401
    default_detail = "Unauthorized exception"
    default_code = "unauthorized_exception"


class ForbiddenEntityException(APIException):
    """
    The forbidden entity exception resource.

    Status code: 403
    Detail: Forbidden exception
    Code: forbidden_exception
    """

    status_code = 403
    default_detail = "Forbidden exception"
    default_code = "forbidden_exception"


class NotFoundException(APIException):
    """
    The not found exception resource.

    Status code: 404
    Detail: Not found exception
    Code: not_found_exception
    """

    status_code = 404
    default_detail = "Not found exception"
    default_code = "not_found_exception"


class UnprocessableEntityException(APIException):
    """
    The unprocessable entity exception resource.

    Status code: 422
    Detail: Unprocessable entity exception
    Code: unprocessable_entity_exception
    """

    status_code = 422
    default_detail = "Unprocessable entity exception"
    default_code = "unprocessable_entity_exception"


class InternalServerErrorException(APIException):
    """
    The internal server error exception resource.

    Status code: 500
    Detail: Internal server error exception
    Code: internal_server_error_exception
    """

    status_code = 500
    default_detail = "Internal server error exception"
    default_code = "internal_server_error_exception"
