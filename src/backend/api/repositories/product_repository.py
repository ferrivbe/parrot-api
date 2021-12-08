"""
File name: product_repository.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from django.utils.timezone import now

from api.models.product import Product
from utils.configurations.constants import GenericConstants
from utils.validations.api_validations import ApiValidations


class ProductRepository:
    """
    The product repository.

    Handles transactions between services and repositories.
    """

    def __init__(self):
        """
        Creates a new instance of ProductRepository class.
        """
        self.validator = ApiValidations()

    def create_product(self, product):
        """
        Creates a product:

        :param ProductSerializer.data product: The product to be created.
        """
        self.validator.is_null(product)

        return Product.objects.create(
            name=product.get(GenericConstants.NAME),
            description=product.get(GenericConstants.DESCRIPTION),
        )

    def delete_product(self, product):
        """
        Deletes logically a product.

        :param Product product: The product to be deleted.
        """
        product.deleted_at = now()
        product.save()

        return product

    def get_product_by_id(self, id):
        """
        Gets products by identifier.

        :param uuid4 id: The product identifier.
        """
        self.validator.is_null(id)

        return Product.objects.filter(id=id, deleted_at=None)

    def get_product_by_name(self, name):
        """
        Gets products by name.

        :param string name: The product name.
        """
        self.validator.is_null_or_empty_string(name)

        return Product.objects.filter(name=name, deleted_at=None)

    def update_product(self, updated_product, product):
        """
        Updates a product by identifier.

        :param ProductSerializer.Data updated_product: The updated product.
        :param Product product: The product to be updated.
        """
        self.validator.is_null(updated_product)
        self.validator.is_null(product)

        product.description = updated_product.get(GenericConstants.DESCRIPTION)
        product.name = updated_product.get(GenericConstants.NAME)
        product.updated_at = now()
        product.save()

        return product
