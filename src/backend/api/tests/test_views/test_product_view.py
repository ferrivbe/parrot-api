"""
File name: test_product_view.py
Author: Fernando Rivera
Creation date: 2021-12-11
"""
from uuid import uuid4

from django.urls import reverse
from django.utils.timezone import now
from rest_framework.test import APITestCase

from api.models.product import Product
from auth_api.models import User


class TestProductByIdView(APITestCase):
    """
    The test product by identifier view class.

    Tests the ProductByIdView class.
    """

    def setup(self):
        """
        TestProductByIdView class setup.
        """
        self.deleted_product_id = uuid4()
        self.product_id = uuid4()
        self.user_id = uuid4()

        self.user = User.objects.create(
            id=self.user_id,
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=2,
        )

        self.deleted_product = Product.objects.create(
            id=self.deleted_product_id,
            name="test_product_name_deleted",
            description="test_product_description_deleted",
            price=100,
            deleted_at=now(),
        )

        self.product = Product.objects.create(
            id=self.product_id,
            name="test_product_name",
            description="test_product_description",
            price=100,
        )

    def test_prodcut_by_id_get(self):
        """
        Tests the GET method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": self.product_id})

        expected_data = {
            "id": self.product_id,
            "name": "test_product_name",
            "description": "test_product_description",
            "price": 100,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # assert
        assert response.status_code == 200
        assert response.data.get("name") == expected_data.get("name")

    def test_product_by_id_get_not_found(self):
        """
        Tests the GET method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": uuid4()})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # assert
        assert response.status_code == 404

    def test_product_by_id_get_not_found_when_logic_delete(self):
        """
        Tests the GET method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": self.deleted_product_id})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # assert
        assert response.status_code == 404

    def test_product_by_id_put(self):
        """
        Tests the PUT method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": self.product_id})
        request_payload = {
            "name": "test_update",
            "description": "test_description_update",
            "price": 101,
        }

        expected_data = {
            "id": self.product_id,
            "name": "test_update",
            "description": "test_description_update",
            "price": 101,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload)

        # assert
        assert response.status_code == 200
        assert response.data.get("name") == expected_data.get("name")

    def test_product_by_id_put_not_found(self):
        """
        Tests the PUT method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": uuid4()})
        request_payload = {
            "name": "test_update",
            "description": "test_description_update",
            "price": 101,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload)

        # assert
        assert response.status_code == 404

    def test_product_by_id_put_not_found_when_logic_delete(self):
        """
        Tests the PUT method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": self.deleted_product_id})
        request_payload = {
            "name": "test_update",
            "description": "test_description_update",
            "price": 101,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload)

        # assert
        assert response.status_code == 404

    def test_product_by_id_put_bad_request_when_wrong_characters(self):
        """
        Tests the PUT method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": self.product_id})
        request_payload = {
            "name": "test_update !",
            "description": "test_description_update !",
            "price": 101,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload)

        # assert
        assert response.status_code == 400

    def test_product_by_id_put_unprocessable_entity_when_price_zero(self):
        """
        Tests the PUT method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": self.product_id})
        request_payload = {
            "name": "test_update",
            "description": "test_description_update",
            "price": 0,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload)

        # assert
        assert response.status_code == 422

    def test_product_by_id_put_unprocessable_entity_when_price_negative(self):
        """
        Tests the PUT method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": self.product_id})
        request_payload = {
            "name": "test_update",
            "description": "test_description_update",
            "price": -10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload)

        # assert
        assert response.status_code == 422

    def test_product_by_id_put_unprocessable_entity_when_name_missing(self):
        """
        Tests the PUT method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": self.product_id})
        request_payload = {
            "description": "test_description_update",
            "price": -10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload)

        # assert
        assert response.status_code == 422

    def test_product_by_id_put_unprocessable_entity_when_name_exists(self):
        """
        Tests the PUT method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": self.product_id})
        request_payload = {
            "name": "test_product_name",
            "description": "test_description_update",
            "price": -10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload)

        # assert
        assert response.status_code == 422

    def test_product_by_id_delete(self):
        """
        Tests the DELETE method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": self.product_id})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # assert
        assert response.status_code == 200
        assert response.data.get("id") == str(self.product_id)

    def test_product_by_id_delete_not_found(self):
        """
        Tests the DELETE method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": uuid4()})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # assert
        assert response.status_code == 404

    def test_product_by_id_delete_not_found_when_logic_delete(self):
        """
        Tests the DELETE method of product by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("products_id", kwargs={"id": self.deleted_product})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # assert
        assert response.status_code == 404


class TestProductView(APITestCase):
    """
    The test product view class.

    Tests the ProductView class.
    """

    def setup(self):
        """
        TestProductByIdView class setup.
        """
        self.product_id = uuid4()
        self.user_id = uuid4()

        self.user = User.objects.create(
            id=self.user_id,
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=2,
        )

        self.product = Product.objects.create(
            id=self.product_id,
            name="test_product_name",
            description="test_product_description",
            price=100,
        )

    def test_product_post(self):
        """
        Tests the POST method of product view.
        """
        # arrange
        self.setup()
        url = reverse("products")
        request_payload = {
            "name": "test_product_name_new",
            "description": "test_description_new",
            "price": 10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload)

        # assert
        assert response.status_code == 201
        assert response.data.get("name") == request_payload.get("name")

    def test_product_post_bad_request_when_wrong_characters_in_name(self):
        """
        Tests the POST method of product view.
        """
        # arrange
        self.setup()
        url = reverse("products")
        request_payload = {
            "name": "test_product_name !",
            "description": "test_description",
            "price": 10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload)

        # assert
        assert response.status_code == 400

    def test_product_post_bad_request_when_wrong_characters_in_description(self):
        """
        Tests the POST method of product view.
        """
        # arrange
        self.setup()
        url = reverse("products")
        request_payload = {
            "name": "test_product_name",
            "description": "test_description !",
            "price": 10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload)

        # assert
        assert response.status_code == 400

    def test_product_post_unprocessable_entity_when_name_exists(self):
        """
        Tests the POST method of product view.
        """
        # arrange
        self.setup()
        url = reverse("products")
        request_payload = {
            "name": "test_product_name",
            "description": "test_description",
            "price": 10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload)

        # assert
        assert response.status_code == 422

    def test_product_post_unprocessable_entity_when_name_missing(self):
        """
        Tests the POST method of product view.
        """
        # arrange
        self.setup()
        url = reverse("products")
        request_payload = {
            "description": "test_description",
            "price": 10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload)

        # assert
        assert response.status_code == 422

    def test_product_post_unprocessable_entity_when_price_zero(self):
        """
        Tests the POST method of product view.
        """
        # arrange
        self.setup()
        url = reverse("products")
        request_payload = {
            "name": "test_product_name",
            "description": "test_description",
            "price": 0,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload)

        # assert
        assert response.status_code == 422

    def test_product_post_unprocessable_entity_when_price_negative(self):
        """
        Tests the POST method of product view.
        """
        # arrange
        self.setup()
        url = reverse("products")
        request_payload = {
            "name": "test_product_name",
            "description": "test_description",
            "price": -10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload)

        # assert
        assert response.status_code == 422
