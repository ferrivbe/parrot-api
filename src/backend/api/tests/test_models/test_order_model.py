"""
File name: test_order_model.py
Author: Fernando Rivera
Creation date: 2021-12-11
"""
from uuid import uuid4

import pytest

from api.models.order import Order
from api.models.product import Product
from api.models.product_quantity import ProductQuantity


@pytest.mark.django_db
class TestOrderModel:
    """
    The test order model class.

    Tests the Order model.
    """

    def test_order_str(self):
        """
        Tests the ProductQuantity model __str__ method.
        """
        # arrange
        id = uuid4()
        product_id = uuid4()
        product_quantity_id = uuid4()

        # act
        Product.objects.create(
            id=product_id,
            name="test_name",
            description="test_descritpion",
        )

        order_created = Order.objects.create(
            id=id,
            total_price=1,
            external_client="test_externa_client",
        )

        ProductQuantity.objects.create(
            id=product_quantity_id,
            order_id=id,
            product_id=product_id,
            quantity=1,
        )

        # assert
        assert order_created.__str__() == str(id)
