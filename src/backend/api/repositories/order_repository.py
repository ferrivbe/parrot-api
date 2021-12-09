"""
File name: order_repository.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from django.utils.timezone import now

from api.models.order import Order
from utils.configurations.constants import GenericConstants
from utils.validations.api_validations import ApiValidations


class OrderRepository:
    """
    The order repository.

    Handles transactions between services and repositories.
    """

    def __init__(self):
        """
        Creates a new instance of OrderRepository class.
        """
        self.validator = ApiValidations()

    def create_order(self, order):
        """
        Creates an order:

        :param OrderSerializer.data order: The order to be created.
        """
        self.validator.is_null(order)

        return Order.objects.create(
            external_client=order.get(GenericConstants.EXTERNAL_CLIENT),
            total_price=order.get(GenericConstants.TOTAL_PRICE),
        )
