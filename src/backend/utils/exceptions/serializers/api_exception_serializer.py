"""
File name: api_exception_serializer.py
Author: Fernando Rivera
Creation date: 2021-07-20
"""
from rest_framework import serializers

from .error_trace_serializer import ErrorTraceSerializer


class ApiExceptionSerializer(serializers.Serializer):
    """
    The API exception serializer.
    """

    error = ErrorTraceSerializer()
    """
    The error.
    """
