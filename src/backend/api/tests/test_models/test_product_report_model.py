"""
File name: test_product_order_model.py
Author: Fernando Rivera
Creation date: 2021-12-11
"""
from uuid import uuid4

import pytest

from api.models.product_report import ProductReport


@pytest.mark.django_db
class TestProductReportModel:
    """
    The test product_report object class.

    Tests the PorductReport object.
    """

    def test_product_report_str(self):
        """
        Tests the ProductReport object __str__ method.
        """
        # arrange
        product_id = uuid4()

        created_product_report = ProductReport(
            id=product_id,
            name="test_name",
            description="test_description",
            total_quantity=1,
            total_price=2,
        )

        # assert
        assert created_product_report.__str__() == str(product_id)
