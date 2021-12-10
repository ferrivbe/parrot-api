"""
File name: user_registration_serializer.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework import serializers

from auth_api.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    The user registration serializer.
    """

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
        ]

    def create(self, validated_data):
        """
        Creates a user registration.
        """
        auth_user = User.objects.create_user(**validated_data)
        return auth_user
