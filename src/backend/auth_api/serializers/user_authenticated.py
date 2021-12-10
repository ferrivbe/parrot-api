"""
File name: user_authenticated.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework import serializers


class UserAuthenticatedSerializer(serializers.Serializer):
    """
    The user authenticated serializer.
    """

    access_token = serializers.CharField(read_only=True)
    """
    The user login access.
    """

    refresh_token = serializers.CharField(read_only=True)
    """
    The user login refresh.
    """

    expires_in = serializers.IntegerField(read_only=True)
    """
    The expiration time.
    """

    role = serializers.CharField(read_only=True)
    """
    The user login role.
    """

    email = serializers.EmailField()
    """
    The user login email.
    """
