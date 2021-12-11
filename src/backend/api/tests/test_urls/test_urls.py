"""
File name: test_urls.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from uuid import uuid4

from django.urls import resolve, reverse


class TestUrls:
    """
    The test urls class.

    Tests the urls in the API app.
    """

    def test_products_url(self):
        """
        Tests the products url.
        """
        path = reverse("products")

        assert resolve(path).view_name == "products"

    def test_products_id_url(self):
        """
        Tests the products_id url.
        """
        path = reverse(
            "products_id",
            kwargs={
                "id": uuid4(),
            },
        )

        assert resolve(path).view_name == "products_id"

    def test_orders_url(self):
        """
        Tests the orders url.
        """
        path = reverse("orders")

        assert resolve(path).view_name == "orders"

    def test_orders_id_url(self):
        """
        Tests the orders_id url.
        """
        path = reverse(
            "orders_id",
            kwargs={
                "id": uuid4(),
            },
        )

        assert resolve(path).view_name == "orders_id"

    def test_orders_id_closures_closures(self):
        """
        Tests the orders_id_closures url.
        """
        path = reverse(
            "orders_id_closures",
            kwargs={
                "id": uuid4(),
            },
        )

        assert resolve(path).view_name == "orders_id_closures"

    def test_orders_product_quantities_closures(self):
        """
        Tests the orders_product_quantities url.
        """
        path = reverse(
            "orders_product_quantities",
            kwargs={
                "order_id": uuid4(),
            },
        )

        assert resolve(path).view_name == "orders_product_quantities"

    def test_orders_product_quantities_id_closures(self):
        """
        Tests the orders_product_quantities_id url.
        """
        path = reverse(
            "orders_product_quantities_id",
            kwargs={
                "order_id": uuid4(),
                "id": uuid4(),
            },
        )

        assert resolve(path).view_name == "orders_product_quantities_id"

    def test_products_reports_url(self):
        """
        Tests the products_reports url.
        """
        path = reverse("products_reports")

        assert resolve(path).view_name == "products_reports"
