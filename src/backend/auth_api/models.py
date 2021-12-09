"""
File name: models.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from auth_api.managers import CustomUserManager
from utils.configurations.constants import GenericConstants


class User(AbstractBaseUser, PermissionsMixin):
    """
    The user object.
    """

    ADMIN = 1
    """
    The auth administrator role choice.
    """

    USER = 2
    """
    The auth user role choice.
    """

    ROLE_CHOICES = ((ADMIN, "Admin"), (USER, "User"))

    id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid4,
        verbose_name="user identifier",
        primary_key=True,
    )
    """
    The user uuid identifier.
    """

    email = models.EmailField()
    """
    The user email.
    """

    first_name = models.CharField(max_length=30, blank=True)
    """
    The user fists name.
    """

    last_name = models.CharField(max_length=50, blank=True)
    """
    The user last name.
    """

    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True, default=3
    )
    """
    The user role.
    """

    is_active = models.BooleanField(default=True)
    """
    The user active flag.
    """

    created_at = models.DateTimeField(default=timezone.now)
    """
    The user creation date.
    """

    updated_at = models.DateTimeField(default=None, null=True)
    """
    The user modification date.
    """

    deleted_at = models.DateTimeField(default=None, null=True)
    """
    The user deletion date.
    """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """
        Returns a string representation
        """
        return self.email

    class Meta:
        db_table = GenericConstants.USER
