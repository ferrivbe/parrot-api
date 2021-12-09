"""
File name: user_login.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework import serializers

from auth_api.models import User


class UserListSerializer(serializers.ModelSerializer):
    """
    The user list serializer.
    """

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "role",
        )
