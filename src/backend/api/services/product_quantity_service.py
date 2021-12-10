"""
File name: product_quantity_service.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from api.repositories.product_quantity_repository import ProductQuantityRepository
from api.repositories.product_repository import ProductRepository
from api.serializers.responses.product_quantity_response_serializer import (
    ProductQuantityResponseSerializer,
)
from utils.configurations.constants import ExceptionConstants, GenericConstants
from utils.exceptions.api_exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)
from utils.validations.api_validations import ApiValidations
from api.repositories.order_repository import OrderRepository


class ProductQuantityService:
    """
    The product quantity service.

    Handles transactions betweem requests and repository.
    """

    def __init__(self):
        """
        Creates a new instance of ProductQuantityService class.
        """
        self.order_repository = OrderRepository()
        self.product_repository = ProductRepository()
        self.repository = ProductQuantityRepository()
        self.validator = ApiValidations()

    def create_product_quantity(self, product_quantity, order_id):
        """
        Creates a product quantity.

        :param ProductQuantitySerializers.data product_quantity: The product quantity to be created.
        :param uuid4 order_id: The order identifier.
        """
        self.validator.is_null(product_quantity)
        self.validator.is_null(order_id)

        self.__validate_product_quantity(product_quantity, order_id)

        created_product_quantity = self.repository.create_product_quantity(
            product_quantity,
            order_id,
            product_quantity.get(GenericConstants.PRODUCT).get(GenericConstants.ID),
        )

        self.__increase_total_price(
            created_product_quantity.product.id,
            created_product_quantity.quantity,
            order_id,
        )

        return ProductQuantityResponseSerializer(
            created_product_quantity,
            many=False,
        )

    def delete_product_quantity_by_id(self, order_id, id):
        """
        Deletes a product quantity by identifier.

        :param uuid4 order_id: The order identifier.
        :param uuid4 id: The product quantity identifier.
        """
        self.validator.is_null(order_id)
        self.validator.is_null(id)

        product_quantity = self.__get_product_quantity_by_id(order_id, id)
        deleted_product_quantity = self.repository.delete_product_quantity(
            product_quantity
        )
        self.__increase_total_price(
            deleted_product_quantity.product.id,
            deleted_product_quantity.quantity * GenericConstants.NEGATIVE_INDEX,
            order_id,
        )

        return ProductQuantityResponseSerializer(
            deleted_product_quantity,
            many=False,
        )

    def get_product_quantity_by_id(self, order_id, id):
        """
        Gets the product quantity by identifier.

        :param uuid4 order_id: The order identifier.
        :param uuid4 id: The product quantity identifier.
        """
        self.validator.is_null(order_id)
        self.validator.is_null(id)

        return ProductQuantityResponseSerializer(
            self.__get_product_quantity_by_id(order_id, id),
            many=False,
        )

    def update_product_quantity_by_id(self, new_product_quantity, order_id, id):
        """
        Updates a product quantity by identifier.

        :param ProductQuantityUpdateSerializer.data product_quantity: The product quantity.
        :param uuid4 order_id: The order identifier.
        :param uuid4 id: The product quantity identifier.
        """
        self.validator.is_null(new_product_quantity)
        self.validator.is_null(order_id)
        self.validator.is_null(id)

        self.__validate_product_quantity_quantity(new_product_quantity)
        product_quantity = self.__get_product_quantity_by_id(order_id, id)
        old_quantity = product_quantity.quantity

        updated_product_quantity = self.repository.update_product_quantity_quantity(
            product_quantity, new_product_quantity.get(GenericConstants.QUANTITY)
        )

        self.__increase_total_price(
            updated_product_quantity.product.id,
            updated_product_quantity.quantity - old_quantity,
            order_id,
        )

        return ProductQuantityResponseSerializer(
            updated_product_quantity,
            many=False,
        )

    def __decrease_total_price(self, id, quantity, order_id):
        """
        Decreases th total price of the order.

        :param uuid id: The product quantity identifier.
        :param int quantity: The product_quantity quantity.
        :param uuid4 order_id: The order identifier.
        """
        product_price = self.__get_product_price(id)
        decreased_price = quantity * product_price

        order = self.__get_order(order_id)
        self.order_repository.update_order_total_price(
            order, order.total_price - decreased_price
        )

    def __get_order(self, id):
        """
        Gets an order.

        :param uuid4 id: The order identifier.
        """
        orders = self.order_repository.get_order_by_id(id)

        if orders.count == 0 or orders is None:
            raise NotFoundException(
                ExceptionConstants.ORDER_NOT_FOUND % {GenericConstants.ID: id}
            )

        return orders.first()

    def __get_product_price(self, id):
        """
        Gets the product price.

        :param uuid4 id: The product identifier.
        """
        self.validator.is_null(id)

        return self.product_repository.get_product_by_id(id).first().price

    def __get_product_quantity_by_id(self, order_id, id):
        """
        Gets a product quantity by identifier.

        :param uuid4 order_id: The order identifier.
        :param uuid4 id: The product quantity identifier.
        """
        self.validator.is_null(order_id)
        self.validator.is_null(id)

        product_quantity = self.repository.get_product_quantity_by_id(order_id, id)

        if product_quantity.count() == 0:
            raise NotFoundException(
                ExceptionConstants.QUANTITY_FOR_PRODUCT_NOT_FOUND
                % {GenericConstants.ID: id}
            )

        return product_quantity.first()

    def __increase_total_price(self, id, quantity, order_id):
        """
        Increases th total price of the order.

        :param uuid id: The product quantity identifier.
        :param int quantity: The product_quantity quantity.
        :param uuid4 order_id: The order identifier.
        """
        product_price = self.__get_product_price(id)
        decreased_price = quantity * product_price

        order = self.__get_order(order_id)
        self.order_repository.update_order_total_price(
            order, order.total_price + decreased_price
        )

    def __validate_product_exists(self, id):
        """
        Validates if product by identifier exsits.

        :param uuid4 id: The product identifier.
        """
        if self.product_repository.get_product_by_id(id).count() == 0:
            raise NotFoundException(
                ExceptionConstants.PRODUCT_BY_ID_NOT_FOUND % {GenericConstants.ID: id}
            )

    def __validate_product_quantity(self, product_quantity, order_id):
        """
        Validates a product quantity.

        :param ProductQuantitySerializers.data product_quantity: The product quantity.
        :param uuid4 order_id: The order identifier.
        """
        self.validator.is_null(product_quantity)
        self.validator.is_null(order_id)

        self.__validate_product_quantity_quantity(product_quantity)

        product_id = product_quantity.get(GenericConstants.PRODUCT).get(
            GenericConstants.ID
        )

        self.__validate_product_exists(product_id)

        product_quantities = (
            self.repository.get_product_quantity_by_order_id_and_product_id(
                order_id, product_id
            )
        )

        if product_quantities.count() != 0:
            raise UnprocessableEntityException(
                ExceptionConstants.QUANTITY_FOR_PRODUCT_EXISTS
                % {GenericConstants.ID: product_id}
            )

    def __validate_product_quantity_quantity(self, product_quantity):
        """
        Validates a product_quantity quantity.

        :param ProductQuantitySerializer.data product_quantity: The product quantity.
        """
        quantity = product_quantity.get(GenericConstants.QUANTITY)

        if quantity <= 0 or quantity is None:
            raise UnprocessableEntityException(
                ExceptionConstants.VALID_QUANTITY_MUST_BE_SET
            )
