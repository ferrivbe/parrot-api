"""
File name: error_trace_serializer.py
Author: Fernando Rivera
Creation date: 2021-07-20
"""
from rest_framework import serializers


class ErrorTraceSerializer(serializers.Serializer):
    """
    The error trace serializer
    """

    event_type = serializers.CharField(max_length=128)
    """
    The error event type.
    """

    status_code = serializers.CharField(max_length=128)
    """
    The error status code.
    """

    message = serializers.CharField(max_length=128)
    """
    The error message.
    """

    target = serializers.CharField(max_length=128)
    """
    The error target.
    """
