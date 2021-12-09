"""
File name: test_product_model.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from uuid import uuid4

import pytest

from api.models.product import Product


@pytest.mark.django_db
class TestProductModel:
    """
    The test product model class.

    Tests the Product model.
    """

    def test_product_str(self):
        """
        Tests the Product model __str__ method.
        """
        # arrange
        id = uuid4()

        # act
        product_created = Product.objects.create(
            id=id, name="test_name", description="test_descritpion"
        )

        # assert
        assert product_created.__str__() == str(id)
