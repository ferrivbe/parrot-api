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

    def create_product_quantity(self, product_quantity, order_id, product_id):
        """
        Creates a product quantity:

        :param ProductQuantitySerializer.dataproduct_quantity: The product quentity to be created.
        :pram uuid4 order_id: The order identifier
        :pram uuid4 product_id: The product identifier
        """
        self.validator.is_null(product_quantity)
        self.validator.is_null(order_id)
        self.validator.is_null(product_id)

        return ProductQuantity.objects.create(
            product_id=product_id,
            quantity=product_quantity.get(GenericConstants.QUANTITY),
            order_id=order_id,
        )

    def get_product_quantity_by_order_id_and_product_id(self, order_id, product_id):
        """
        Gets a product quantity by order identifier and product identifier.

        :pram uuid4 order_id: The order identifier
        :pram uuid4 product_id: The product identifier
        """
        self.validator.is_null(order_id)
        self.validator.is_null(product_id)

        return ProductQuantity.objects.filter(
            order_id=order_id,
            product_id=product_id,
            deleted_at=None,
        )

    def delete_product_quantity_by_order_id(self, order_id):
        """
        Deletes product quantities by order identifier.

        :param uuid4 order_id: The order identifier.
        """
        self.validator.is_null(order_id)

        product_quantities = ProductQuantity.objects.filter(
            order_id=order_id,
            deleted_at=None,
        ).update(deleted_at=now())

        return product_quantities

    def update_product_quantity_quantity(self, product_quantity, new_quantity):
        """
        Updates a product_quantity quantity.

        :param ProductQuantity product_quantity: The product quantity to be updated.
        :param int new_quantity: The new quantity to be updated.
        """
        self.validator.is_null(product_quantity)
        self.validator.is_null(new_quantity)

        product_quantity.quantity = product_quantity.quantity + new_quantity
        product_quantity.updated_at = now()
        product_quantity.save()

        return product_quantity
