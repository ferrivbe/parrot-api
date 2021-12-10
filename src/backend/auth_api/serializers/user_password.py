"""
File name: user_password.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework import serializers

from auth_api.models import User


class UserPasswordSerializer(serializers.ModelSerializer):
    """
    The user password serializer.
    """

    class Meta:
        model = User
        fields = [
            "password",
        ]
