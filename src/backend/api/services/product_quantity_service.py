"""
File name: product_quantity_service.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from api.repositories.product_quantity_repository import ProductQuantityRepository
from api.serializers.responses.product_response_serializer import (
    ProductResponseSerializer,
)
from utils.configurations.constants import ExceptionConstants, GenericConstants
from utils.exceptions.api_exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)
from utils.validations.api_validations import ApiValidations


class ProductQuantityService:
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
        self.__validate_product_price(price)

        return ProductResponseSerializer(
            self.repository.create_product(product), many=False
        )
