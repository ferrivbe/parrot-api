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

    def test_product_url(self):
        """
        Tests the menu url.
        """
        path = reverse("products")

        assert resolve(path).view_name == "products"

    def test_menus_id_url(self):
        """
        Tests the menu_id url.
        """
        path = reverse("products_id", kwargs={"id": uuid4()})

        assert resolve(path).view_name == "products_id"
