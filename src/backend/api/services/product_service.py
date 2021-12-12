"""
File name: product_service.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from api.repositories.product_repository import ProductRepository
from api.serializers.responses.product_response_serializer import (
    ProductResponseSerializer,
)
from utils.configurations.constants import ExceptionConstants, GenericConstants
from utils.exceptions.api_exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)
from utils.validations.api_validations import ApiValidations


class ProductService:
    """
    The product service.

    Handles transactions betweem requests and repository.
    """

    def __init__(self):
        """
        Creates a new instance of ProductService class.
        """
        self.repository = ProductRepository()
        self.validator = ApiValidations()

    def create_product(self, product):
        """
        Creates a product.

        :param ProdcutSerializer.data product: The product to be created.
        """
        self.validator.is_null(product)

        name = product.get(GenericConstants.NAME)
        price = product.get(GenericConstants.PRICE)

        self.__validate_product_by_name(name)
        self.repository.validate_product_price(price)

        return ProductResponseSerializer(
            self.repository.create_product(product), many=False
        )

    def delete_product_by_id(self, id):
        """
        Deletes a product by identifier.

        :param uuid4 id: The product identifier.
        """
        self.validator.is_null(id)

        products = self.__validate_product_by_id(id)

        return ProductResponseSerializer(
            self.repository.delete_product(products.first()), many=False
        )

    def get_product_by_id(self, id):
        """
        Gets product by identifier.

        :param uuid4 id: The product identifier.
        """
        self.validator.is_null(id)

        products = self.__validate_product_by_id(id)

        return ProductResponseSerializer(products.first(), many=False)

    def update_product(self, product, id):
        """
        Updates a product by identifier.

        :param ProductSerializer.Data product: The product.
        :param uuid4 id: The product identifier.
        """
        self.validator.is_null(product)
        self.validator.is_null(id)

        name = product.get(GenericConstants.NAME)
        price = product.get(GenericConstants.PRICE)

        products = self.__validate_product_by_id(id)
        self.__validate_product_by_name(name)
        self.repository.validate_product_price(price)

        return ProductResponseSerializer(
            self.repository.update_product(product, products.first()), many=False
        )

    def __validate_product_by_id(self, id):
        """
        Validates if product exists.

        :param Product[] products: The products.
        :param uuid4 id: The product identifier.
        """
        products = self.repository.get_product_by_id(id)

        if products.count() == 0:
            raise NotFoundException(
                ExceptionConstants.PRODUCT_BY_ID_NOT_FOUND % {GenericConstants.ID: id}
            )

        return products

    def __validate_product_by_name(self, name):
        """
        Validates if product by name exists.

        :param Product[] products: The products.
        :param string name: The product name.
        """
        if name is None or name == GenericConstants.EMPTY_CHAR:
            raise UnprocessableEntityException(
                ExceptionConstants.PRODUCT_NAME_IS_REQUIRED
            )

        products = self.repository.get_product_by_name(name)

        if products.count() != 0:
            raise UnprocessableEntityException(
                ExceptionConstants.PRODUCT_BY_NAME_EXISTS
                % {GenericConstants.NAME: name}
            )
