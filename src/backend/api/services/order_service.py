"""
File name: order_service.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from api.repositories.order_repository import OrderRepository
from api.repositories.product_quantity_repository import ProductQuantityRepository
from api.serializers.responses.order_response_serializer import OrderResponseSerializer
from utils.configurations.constants import ExceptionConstants, GenericConstants
from utils.exceptions.api_exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)
from utils.validations.api_validations import ApiValidations


class OrderService:
    """
    The product service.

    Handles transactions betweem requests and repository.
    """

    def __init__(self):
        """
        Creates a new instance of OrderService class.
        """
        self.product_quantity_repository = ProductQuantityRepository()
        self.repository = OrderRepository()
        self.validator = ApiValidations()

    def create_order(self, order):
        """
        Creates an order.

        :param OrderSerializer.data order: The order to be created.
        """
        self.validator.is_null(order)

        external_client = order.get(GenericConstants.EXTERNAL_CLIENT)
        self.product_quantity_repository.create_product_quantity(
            order.get(
                GenericConstants.PRODUCT_QUANTITY,
            )
        )

        return OrderResponseSerializer(self.repository.create_order(order), many=False)
