"""
File name: order_repository.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from django.db.models.query import Prefetch
from django.utils.timezone import now

from api.models.order import Order
from api.models.product_quantity import ProductQuantity
from utils.configurations.constants import ExceptionConstants, GenericConstants
from utils.exceptions.api_exceptions import UnprocessableEntityException
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

    def delete_order(self, order):
        """
        Deletes an order.

        :param Order order:The order to be deleted.
        """
        self.validator.is_null(order)

        order.deleted_at = now()
        order.save()

        return order

    def get_order_by_id(self, id):
        """
        Gets an order by identifier.

        :param uuid4 id: The order identifier.
        """
        self.validator.is_null(id)

        return Order.objects.filter(id=id, deleted_at=None).prefetch_related(
            Prefetch(
                "product_quantities",
                queryset=ProductQuantity.objects.filter(deleted_at=None),
            )
        )

    def update_order_external_client(self, order, external_client):
        """
        Updates the order external client.

        :param Order order: The order to be updated.
        :param string external_client: The new external client.
        """
        self.validator.is_null(order)
        self.validator.is_null_or_empty_string(external_client)

        order.external_client = external_client
        order.updated_at = now()
        order.save()

        return order

    def update_order_total_price(self, order, total_price):
        """
        Updates the order total price.

        :param Order order: The order to be updated.
        :param int total_price: The total price.
        """
        self.validator.is_null(order)
        self.validator.is_null(total_price)

        order.total_price = total_price
        order.updated_at = now()
        order.save()

        return order

    def update_order_closure(self, order):
        """
        Updates the order closure.

        :param Order order: The order to be closed.
        """
        self.validator.is_null(order)

        order.closed_at = now()
        order.updated_at = now()
        order.save()

        return order

    def validate_order_closed(self, order):
        """
        Validates if order is closed.
        If order is closed, no further changes are allowed.

        :param Order order: The order to be validated.
        """
        if order.closed_at is not None:
            raise UnprocessableEntityException(
                ExceptionConstants.ORDER_IS_CLOSED % {GenericConstants.ID: order.id}
            )
