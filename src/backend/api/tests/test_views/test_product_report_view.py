"""
File name: test_product_report_view.py
Author: Fernando Rivera
Creation date: 2021-12-12
"""
from uuid import uuid4

from django.urls import reverse
from django.utils.timezone import now
from rest_framework.test import APITestCase

from api.models.order import Order
from api.models.product import Product
from api.models.product_quantity import ProductQuantity
from auth_api.models import User


class TestProductReportView(APITestCase):
    """
    The test product report view class.

    Tests the ProductReportView class.
    """

    def setup(self):
        """
        TestProductReportView class setup.
        """
        self.product_id = uuid4()
        self.product_quantity_id = uuid4()
        self.order_id = uuid4()

        self.product, self.product_quantity, self.order = self.create_models(
            self.product_id,
            self.product_quantity_id,
            self.order_id,
            None,
            None,
        )

        self.deleted_product_id = uuid4()
        self.deleted_product_quantity_id = uuid4()
        self.deleted_order_id = uuid4()

        (
            self.deleted_product,
            self.deleted_product_quantity,
            self.deleted_order,
        ) = self.create_models(
            self.deleted_product_id,
            self.deleted_product_quantity_id,
            self.deleted_order_id,
            now(),
            None,
        )

        self.closed_product_id = uuid4()
        self.closed_product_quantity_id = uuid4()
        self.closed_order_id = uuid4()

        (
            self.closed_product,
            self.closed_product_quantity,
            self.closed_order,
        ) = self.create_models(
            self.closed_product_id,
            self.closed_product_quantity_id,
            self.closed_order_id,
            None,
            now(),
        )

        self.user_id = uuid4()

        self.user = User.objects.create(
            id=self.user_id,
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=2,
        )

    def create_models(
        self, product_id, product_quantity_id, order_id, deleted_at, closed_at
    ):
        """
        Creates a Product.

        :param uuid4 product_id: The product identifier.
        :param uuid4 product_quantity_id: The product quantity identifier.
        :param uuid4 order_id: The order identifier.
        :param datetime deleted_at: The order deletion date.
        :param datetime closed_at: The order closing date.
        """
        return (
            Product.objects.create(
                id=product_id,
                name="test_product_name",
                description="test_product_description",
                price=100,
            ),
            Order.objects.create(
                id=order_id,
                external_client="test_external_client",
                total_price=100,
                closed_at=closed_at,
                deleted_at=deleted_at,
            ),
            ProductQuantity.objects.create(
                id=product_quantity_id,
                product_id=product_id,
                order_id=order_id,
                quantity=10,
            ),
        )

    def test_product_report_get(self):
        """
        Tests the GET method of product report view.
        """
        # arrange
        self.setup()
        url = reverse("products_reports")

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # assert
        assert response.status_code == 200

    def test_product_report_get_not_found(self):
        """
        Tests the GET method of product report view.
        """
        # arrange
        self.setup()
        url = "products/reports?end_date=2020-01-01T03:02:01.023"

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # assert
        assert response.status_code == 404
