"""
File name: product_quantity.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from uuid import uuid4

from django.db import models
from django.utils.timezone import now

from api.models.order import Order
from api.models.product import Product
from utils.configurations.constants import GenericConstants


class ProductQuantity(models.Model):
    """
    The product quantity data contract.
    """

    id = models.UUIDField(default=uuid4, primary_key=True)
    """
    The product quantity identifier.
    """

    order = models.ForeignKey(
        Order,
        related_name=GenericConstants.PRODUCT_QUANTITIES,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        related_name=GenericConstants.PRODUCT_QUANTITY,
        on_delete=models.CASCADE,
    )
    """
    The product name.
    """

    quantity = models.IntegerField(null=True)
    """
    The product quantity.
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
        Represents the object ProductQuantity.
        """
        return str(self.id)

    class Meta:
        db_table = GenericConstants.PRODUCT_QUANTITY
