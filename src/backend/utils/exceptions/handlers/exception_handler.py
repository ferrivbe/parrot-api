"""
File name: exception.py
Author: Fernando Rivera
Creation date: 2021-07-19
"""
import logging

from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler

from ...configurations.constants import GenericConstants

logger = logging.getLogger(__name__)


def handler(exc, context):
    """
    Exception handler.
    """
    response = exception_handler(exc, context)

    if response is not None:
        request = context["request"]

        message = __message_builder(exc.detail)

        error_trace = {
            "event_type": request.method,
            "status_code": exc.status_code,
            "message": message,
            "target": "http://"
            + __evaluate_string(request.META.get("HTTP_HOST"))
            + __evaluate_string(request.get_full_path()),
        }
        response.data.clear()
        response.data["error"] = error_trace

    return response


def __message_builder(detail):
    """
    The exception message builder.
    """
    message = "Something went wrong."

    if isinstance(detail, str):
        message = detail
    elif isinstance(detail, dict):
        if isinstance(detail.get("detail"), ErrorDetail):
            message = detail["detail"]
        else:
            message = str(detail)

    return message


def __evaluate_string(string):
    """
    Evaluates a string, if none returns empty string.
    """
    if string is None:
        return GenericConstants.EMPTY_CHAR

    return str(string)
