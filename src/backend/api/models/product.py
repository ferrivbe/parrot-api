"""
File name: product.py
Author: Fernando Rivera
Creation date: 2021-12-07
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


class Product(models.Model):
    """
    The product data contract.
    """

    id = models.UUIDField(default=uuid4, primary_key=True)
    """
    The product identifier.
    """

    name = models.CharField(
        max_length=32,
        null=True,
        validators=[
            RegexValidator(
                regex=ValidationConstants.LATIN_SPECIAL_CHAR_REGEX,
                message=ExceptionConstants.PARAMETER_INVALID_BY_REGEX,
            ),
        ],
    )
    """
    The product name.
    """

    description = models.CharField(
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
    The product description.
    """

    price = models.IntegerField(null=True)
    """
    The product price.
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
        Represents the object Product.
        """
        return str(self.id)

    class Meta:
        db_table = GenericConstants.PRODUCT
