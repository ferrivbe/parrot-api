"""
File name: product_quantity_repository.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from django.utils.timezone import now

from api.models.product_quantity import ProductQuantity
from utils.configurations.constants import GenericConstants
from utils.validations.api_validations import ApiValidations


class ProductQuantityRepository:
    """
    The product quantity repository.

    Handles transactions between services and repositories.
    """

    def __init__(self):
        """
        Creates a new instance of ProductQuantityRepository class.
        """
        self.validator = ApiValidations()

    def create_product_quantity(self, product_quantity, order_id):
        """
        Creates a product quantity:

        :param ProductQuantitySerializer.dataproduct_quantity: The product quentity to be created.
        """
        self.validator.is_null(product_quantity)

        return ProductQuantity.objects.create(
            product=product_quantity.get(GenericConstants.PRODUCT),
            quantity=product_quantity.get(GenericConstants.QUANTITY),
            order=order_id,
        )
