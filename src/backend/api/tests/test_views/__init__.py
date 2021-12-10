"""
File name: test_product_view.py
Author: Fernando Rivera
Creation date: 2021-12-09
"""
from uuid import uuid4

from django.urls import reverse
from rest_framework.test import APITestCase

from api.models.product import Product


class TestProductByIdView(APITestCase):
    """
    The test product by identifier view class.
    Tests the ProductByIdView class.
    """

    def setup(self):
        """
        Class setup.
        """
        self.product_id = uuid4()

        self.product = Product.objects.create(
            id=self.product_id,
            description="test_description",
            name="test_name",
        )

    def test_product_by_id_get(self):
        """
        Tests the GET method of product by identifier view.
        """
        # arrage
        self.setup()
        url = reverse("products_id", kwargs={"id": self.product_id})

        expected_data = {"name": "test_name", "description": "test_description"}

        # act
        # self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # assert
        assert response.status_code == 200
        assert response.data == expected_data
