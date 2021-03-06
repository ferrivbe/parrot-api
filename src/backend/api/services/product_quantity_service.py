"""
File name: product_quantity_service.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from operator import attrgetter

from api.models.product_report import ProductReport
from api.repositories.order_repository import OrderRepository
from api.repositories.product_quantity_repository import ProductQuantityRepository
from api.repositories.product_repository import ProductRepository
from api.serializers.responses.product_quantity_response_serializer import (
    ProductQuantityResponseSerializer,
)
from api.serializers.responses.product_report_response_serializer import (
    ProductReportResponseSerializer,
)
from utils.configurations.constants import ExceptionConstants, GenericConstants
from utils.exceptions.api_exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)
from utils.validations.api_validations import ApiValidations


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
        order = self.__get_order(order_id)
        self.order_repository.validate_order_closed(order)

        created_product_quantity = self.repository.create_product_quantity(
            product_quantity,
            order_id,
            product_quantity.get(GenericConstants.PRODUCT).get(GenericConstants.ID),
        )

        self.__increase_total_price(
            created_product_quantity.product.id,
            created_product_quantity.quantity,
            order,
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
        order = self.__get_order(order_id)
        self.order_repository.validate_order_closed(order)

        deleted_product_quantity = self.repository.delete_product_quantity(
            product_quantity
        )
        self.__increase_total_price(
            deleted_product_quantity.product.id,
            deleted_product_quantity.quantity * GenericConstants.NEGATIVE_INDEX,
            order,
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

    def get_product_quantity_by_order_closure_date(self, start_date, end_date):
        """
        Gets the product quantity by order closure start and end dates.

        :param datetime start_date: The filter start date.
        :param datetime end_date: The filter end date.
        """
        self.validator.is_null(start_date)
        self.validator.is_null(end_date)

        product_quantities = self.repository.get_product_quantity_by_order_closure_date(
            start_date,
            end_date,
        )
        self.__validate_product_quantity_exists(
            product_quantities,
            start_date,
            end_date,
        )

        product_totals = []

        for product_quantity in product_quantities:
            found_product_total = self.__find_product_total(
                product_totals, product_quantity.product.id
            )

            if found_product_total is not None:
                self.__update_product_total(
                    product_totals,
                    found_product_total,
                    product_quantity,
                )
            else:
                product_totals.append(self.__create_product_total(product_quantity))
        product_totals.sort(key=attrgetter("total_quantity"), reverse=True)

        return ProductReportResponseSerializer(product_totals, many=True).data

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

        order = self.__get_order(order_id)
        self.order_repository.validate_order_closed(order)

        updated_product_quantity = self.repository.update_product_quantity_quantity(
            product_quantity, new_product_quantity.get(GenericConstants.QUANTITY)
        )

        self.__increase_total_price(
            updated_product_quantity.product.id,
            updated_product_quantity.quantity - old_quantity,
            order,
        )

        return ProductQuantityResponseSerializer(
            updated_product_quantity,
            many=False,
        )

    def __create_product_total(self, product_quantity):
        """
        Creates a product report object.

        :param ProductQuantity product_quantity: The product quantity.
        """
        self.validator.is_null(product_quantity)

        return ProductReport(
            id=product_quantity.product.id,
            name=product_quantity.product.name,
            description=product_quantity.product.description,
            total_quantity=product_quantity.quantity,
            total_price=product_quantity.quantity * product_quantity.product.price,
        )

    def __find_product_total(self, product_totals, product_id):
        """
        Finds a product total form list.

        :param ProductReport[] prodcut_totals: The product totals list.
        :param uuid4 product_id: The product identifier.
        """
        self.validator.is_null(product_totals)
        self.validator.is_null(product_id)

        return next(
            (
                product_total
                for product_total in product_totals
                if product_total.id == product_id
            ),
            None,
        )

    def __get_order(self, id):
        """
        Gets an order.

        :param uuid4 id: The order identifier.
        """
        orders = self.order_repository.get_order_by_id(id)

        if orders.count() == 0 or orders is None:
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

        products = self.product_repository.get_product_by_id(id)
        if products.count() == 0:
            raise UnprocessableEntityException(
                ExceptionConstants.PRODUCT_NOT_AVAILABLE % {GenericConstants.ID: id}
            )

        return products.first().price

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

    def __increase_total_price(self, id, quantity, order):
        """
        Increases th total price of the order.

        :param uuid id: The product quantity identifier.
        :param int quantity: The product_quantity quantity.
        :param Order order: The order to be updated.
        """
        product_price = self.__get_product_price(id)
        decreased_price = quantity * product_price

        self.order_repository.update_order_total_price(
            order, order.total_price + decreased_price
        )

    def __update_product_total(
        self, product_totals, found_product_total, product_quantity
    ):
        """
        Updates a product total.

        :param ProductReport[] product totals: The product totals list.
        :param ProductReport found_product_total: The found product total in list.
        :param ProductQuantity product_quantity: The product quantity to be updated.
        """
        self.validator.is_null(product_totals)
        self.validator.is_null(found_product_total)
        self.validator.is_null(product_quantity)

        index = product_totals.index(found_product_total)
        product_totals[index].total_quantity = (
            product_totals[index].total_quantity + product_quantity.quantity
        )
        product_totals[index].total_price = product_totals[index].total_price + (
            product_quantity.quantity * product_quantity.product.price
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

    def __validate_product_quantity_exists(
        self, product_quantities, start_date, end_date
    ):
        """
        Validates if product quantities exist.

        :param ProductQauntity[] product_quantities: The product quantities to be verified.
        :param datetime start_date: The start date.
        :param datetime end_date: The end date.
        """
        if product_quantities.count() == 0:
            raise NotFoundException(
                ExceptionConstants.QUANTITY_FOR_PRODUCT_NOT_FOUND_BY_DATE
                % {
                    GenericConstants.START_DATE: start_date,
                    GenericConstants.END_DATE: end_date,
                }
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
