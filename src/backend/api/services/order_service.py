"""
File name: order_service.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from api.repositories.order_repository import OrderRepository
from api.repositories.product_quantity_repository import ProductQuantityRepository
from api.repositories.product_repository import ProductRepository
from api.serializers.responses.order_response_serializer import OrderResponseSerializer
from utils.configurations.constants import ExceptionConstants, GenericConstants
from utils.exceptions.api_exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)
from utils.validations.api_validations import ApiValidations
from django.core.serializers import serialize


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
        self.product_repository = ProductRepository()
        self.repository = OrderRepository()
        self.validator = ApiValidations()

    def create_order(self, order):
        """
        Creates an order.

        :param OrderSerializer.data order: The order to be created.
        """
        self.validator.is_null(order)

        created_order = self.repository.create_order(order)
        total_price = 0

        self.__validate_order(order)

        for product_quantity in order.get(GenericConstants.PRODUCT_QUANTITIES):
            product = product_quantity.get(GenericConstants.PRODUCT)

            product_id, product_price = self.__create_product(product)
            product_quantity_quantity = self.__create_product_quantity(
                created_order.id,
                product_id,
                product_quantity,
            )

            total_price = total_price + (product_price * product_quantity_quantity)

        return OrderResponseSerializer(
            self.__update_order_total_price(
                created_order,
                total_price,
            ),
            many=False,
        )

    def delete_order_by_id(self, id):
        """
        Deletes an order by identifier.

        :param uuid4 id:The order identifier.
        """
        self.validator.is_null(id)

        orders = self.repository.get_order_by_id(id)
        self.__validate_order_exists(orders, id)
        deleted_order = self.repository.delete_order(orders.first())

        self.product_quantity_repository.delete_product_quantity_by_order_id(id)

        return OrderResponseSerializer(deleted_order, many=False)

    def update_order_by_id(self, order, id):
        """
        Updates an order by identifier.

        :param OrderSerializer.data order: The new order.
        :param uuid4 id: The order identifier.
        """
        self.validator.is_null(order)
        self.validator.is_null(id)

        orders = self.repository.get_order_by_id(id)
        self.__validate_order_exists(orders, id)
        self.__validate_order(order)

        updated_order = self.repository.update_order_external_client(
            orders.first(),
            order.get(GenericConstants.EXTERNAL_CLIENT),
        )

        return OrderResponseSerializer(
            updated_order,
            many=False,
        )

    def get_order_by_id(self, id):
        """
        Gets an order by identifier.

        :param uuid4 id:The order identifier.
        """
        self.validator.is_null(id)

        orders = self.repository.get_order_by_id(id)
        self.__validate_order_exists(orders, id)

        return OrderResponseSerializer(orders.first(), many=False)

    def __create_product(self, product):
        """
        Creates a product if not exists.

        :param ProductSerializer.data product: The product to be creates
        """
        existing_product = self.product_repository.get_product_by_name(
            product.get(GenericConstants.NAME)
        )

        if existing_product.count() == 0:
            self.product_repository.validate_product_price(
                product.get(GenericConstants.PRICE)
            )
            product = self.product_repository.create_product(product)

            return product.id, product.price
        else:

            return existing_product.first().id, existing_product.first().price

    def __create_product_quantity(self, order_id, product_id, product_quantity):
        """
        Creates a product quantity or updates the quantity.

        :param uuid4 order_id: The order identifier.
        :param uuid4 product_id: The product identifier.
        :param ProductQuantitySerializer.data product_quantity: The product quantity.
        """
        existing_product_quantity = self.product_quantity_repository.get_product_quantity_by_order_id_and_product_id(
            order_id,
            product_id,
        )

        if existing_product_quantity.count() == 0:
            return self.product_quantity_repository.create_product_quantity(
                product_quantity,
                order_id,
                product_id,
            ).quantity
        else:
            self.product_quantity_repository.update_product_quantity_quantity(
                existing_product_quantity.first(),
                product_quantity.get(GenericConstants.QUANTITY),
            )

            return product_quantity.get(GenericConstants.QUANTITY)

    def __update_order_total_price(self, order, total_price):
        """
        Updates an order total price.

        :param Order order: The order to be updated.
        :param int total_price: The total price.
        """
        return self.repository.update_order_total_price(order, total_price)

    def __validate_order(self, order):
        """
        Validates an order.

        :param OrderSerializer.data order: The order to validate.
        """
        self.validator.is_null(order)

        if order.get(GenericConstants.EXTERNAL_CLIENT) is None:
            raise UnprocessableEntityException(
                ExceptionConstants.EXTERNAL_CLIENT_NAME_MISSING
            )

    def __validate_order_exists(self, order, id):
        """
        Validates if order exists.

        :param Order[] order: The orders to be validated.
        :param uuid4 id: The order identifier.
        """
        self.validator.is_null(order)
        self.validator.is_null(id)

        if order.count() == 0:
            raise NotFoundException(
                ExceptionConstants.ORDER_NOT_FOUND % {GenericConstants.ID: id}
            )
