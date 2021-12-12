"""
File name: test_product_quantity_model.py
Author: Fernando Rivera
Creation date: 2021-12-11
"""
from uuid import uuid4

import pytest

from api.models.order import Order
from api.models.product import Product
from api.models.product_quantity import ProductQuantity


@pytest.mark.django_db
class TestProductQuantityModel:
    """
    The test product_quantity model class.

    Tests the ProductQuantity model.
    """

    def test_product_quantity_str(self):
        """
        Tests the ProductQuantity model __str__ method.
        """
        # arrange
        id = uuid4()
        order_id = uuid4()
        product_id = uuid4()

        # act
        Product.objects.create(
            id=product_id,
            name="test_name",
            description="test_descritpion",
        )

        Order.objects.create(
            id=order_id,
            total_price=1,
            external_client="test_externa_client",
        )

        product_quantity_created = ProductQuantity.objects.create(
            id=id,
            order_id=order_id,
            product_id=product_id,
            quantity=1,
        )

        # assert
        assert product_quantity_created.__str__() == str(id)
