"""
File name: order.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from uuid import uuid4

from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now

from utils.configurations.constants import (
    ExceptionConstants,
    GenericConstants,
    ValidationConstants,
)


class Order(models.Model):
    """
    The order data contract.
    """

    id = models.UUIDField(default=uuid4, primary_key=True)
    """
    The order identifier.
    """

    total_price = models.IntegerField(null=True)
    """
    The order total price.
    """

    external_client = models.CharField(
        max_length=128,
        null=True,
        validators=[
            RegexValidator(
                regex=ValidationConstants.LATIN_SPECIAL_CHAR_REGEX,
                message=ExceptionConstants.PARAMETER_INVALID_BY_REGEX,
            ),
        ],
    )
    """
    The external client, personal name or otherwise.
    """

    closed_at = models.DateTimeField(default=None, null=True)
    """
    The closing data, determines when order was closed.
    """

    created_at = models.DateTimeField(default=now, editable=False)
    """
    The creation date.
    """

    updated_at = models.DateTimeField(default=None, null=True)
    """
    The modification date.
    """

    deleted_at = models.DateTimeField(default=None, null=True)
    """
    The deletion date.
    """

    def __str__(self):
        """
        Represents the object Order.
        """
        return str(self.id)

    class Meta:
        db_table = GenericConstants.ORDER
