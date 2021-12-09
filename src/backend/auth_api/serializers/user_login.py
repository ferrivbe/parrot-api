"""
File name: user_login.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework import serializers

from auth_api.models import User


class UserLoginSerializer(serializers.ModelSerializer):
    """
    The user login serializer.
    """

    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]
