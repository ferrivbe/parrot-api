"""
File name: test_product_quantity_view.py
Author: Fernando Rivera
Creation date: 2021-12-11
"""
from uuid import uuid4

from django.urls import reverse
from django.utils.timezone import now
from rest_framework.test import APITestCase

from api.models.order import Order
from api.models.product import Product
from api.models.product_quantity import ProductQuantity
from auth_api.models import User


class TestProductQuantityByIdView(APITestCase):
    """
    The test product quantity by identifier view class.

    Tests the ProductQuantityByIdView class.
    """

    def setup(self):
        """
        TestProductQuantityByIdView class setup.
        """
        self.deleted_product_id = uuid4()
        self.deleted_product_quantity_id = uuid4()
        self.deleted_order_id = uuid4()
        self.closed_product_quantity_id = uuid4()
        self.closed_order_id = uuid4()
        self.order_id = uuid4()
        self.product_id = uuid4()
        self.product_quantity_id = uuid4()
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

        self.order = Order.objects.create(
            id=self.order_id,
            external_client="test_external_client",
            total_price=100,
        )

        self.deleted_order = Order.objects.create(
            id=self.deleted_order_id,
            external_client="test_external_client",
            total_price=100,
            deleted_at=now(),
        )

        self.closed_order = Order.objects.create(
            id=self.closed_order_id,
            external_client="test_external_client",
            total_price=100,
            closed_at=now(),
        )

        self.closed_product_quantity = ProductQuantity.objects.create(
            id=self.closed_product_quantity_id,
            product_id=self.product_id,
            order_id=self.closed_order_id,
            quantity=10,
        )

        self.deleted_product_quantity = ProductQuantity.objects.create(
            id=self.deleted_product_quantity_id,
            product_id=self.deleted_product_id,
            order_id=self.deleted_order_id,
            quantity=10,
            deleted_at=now(),
        )

        self.product_quantity = ProductQuantity.objects.create(
            id=self.product_quantity_id,
            product_id=self.product_id,
            order_id=self.order_id,
            quantity=10,
        )

    def test_product_quantity_by_id_get(self):
        """
        Tests the GET method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={"order_id": self.order_id, "id": self.product_quantity_id},
        )

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # assert
        assert response.status_code == 200
        assert response.data.get("id") == str(self.product_quantity_id)

    def test_product_quantity_by_id_get_not_found(self):
        """
        Tests the GET method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={"order_id": self.order_id, "id": uuid4()},
        )

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # assert
        assert response.status_code == 404

    def test_product_quantity_by_id_get_not_found_when_logic_delete(self):
        """
        Tests the GET method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={"order_id": self.order_id, "id": self.deleted_product_quantity_id},
        )

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # assert
        assert response.status_code == 404

    def test_product_quantity_by_id_put(self):
        """
        Tests the PUT method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={"order_id": self.order_id, "id": self.product_quantity_id},
        )

        request_payload = {"quantity": 100}

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, request_payload)

        # assert
        assert response.status_code == 200
        assert response.data.get("id") == str(self.product_quantity_id)

    def test_product_quantity_by_id_put_not_found(self):
        """
        Tests the PUT method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={"order_id": self.order_id, "id": uuid4()},
        )

        request_payload = {"quantity": 100}

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, request_payload)

        # assert
        assert response.status_code == 404

    def test_product_quantity_by_id_put_not_found_when_logic_update(self):
        """
        Tests the PUT method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={"order_id": self.order_id, "id": self.deleted_product_quantity_id},
        )

        request_payload = {"quantity": 100}

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, request_payload)

        # assert
        assert response.status_code == 404

    def test_product_quantity_by_id_put_unprocessable_entity_when_quantity_zero(self):
        """
        Tests the PUT method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={"order_id": self.order_id, "id": self.product_quantity_id},
        )

        request_payload = {"quantity": 0}

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload)

        # assert
        assert response.status_code == 422

    def test_product_quantity_by_id_put_unprocessable_entity_when_quantity_negative(
        self,
    ):
        """
        Tests the PUT method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={"order_id": self.order_id, "id": self.product_quantity_id},
        )

        request_payload = {"quantity": -10}

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload)

        # assert
        assert response.status_code == 422

    def test_product_quantity_by_id_put_unprocessable_entity_when_order_closed(
        self,
    ):
        """
        Tests the PUT method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={
                "order_id": self.closed_order_id,
                "id": self.closed_product_quantity_id,
            },
        )

        request_payload = {"quantity": 10}

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload)

        # assert
        assert response.status_code == 422

    def test_product_quantity_by_id_put_bad_request(
        self,
    ):
        """
        Tests the PUT method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={
                "order_id": self.closed_order_id,
                "id": self.closed_product_quantity_id,
            },
        )

        request_payload = {"quantity": "bad request"}

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload)

        # assert
        assert response.status_code == 400

    def test_product_quantity_by_id_delete(self):
        """
        Tests the DELETE method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={"order_id": self.order_id, "id": self.product_quantity_id},
        )

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # assert
        assert response.status_code == 200

    def test_product_quantity_by_id_delete_not_found(self):
        """
        Tests the DELETE method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={"order_id": self.order_id, "id": uuid4()},
        )

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # assert
        assert response.status_code == 404

    def test_product_quantity_by_id_delete_not_found_when_logical_delete(self):
        """
        Tests the DELETE method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={"order_id": self.order_id, "id": self.deleted_product_quantity_id},
        )

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # assert
        assert response.status_code == 404

    def test_product_quantity_by_id_delete_unprocessable_entity(self):
        """
        Tests the DELETE method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities_id",
            kwargs={
                "order_id": self.closed_order_id,
                "id": self.closed_product_quantity_id,
            },
        )

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # assert
        assert response.status_code == 422


class TestProductQuantityView(APITestCase):
    """
    The test product quantity by identifier view class.

    Tests the ProductQuantityByIdView class.
    """

    def setup(self):
        """
        TestProductQuantityByIdView class setup.
        """
        self.deleted_product_id = uuid4()
        self.deleted_product_quantity_id = uuid4()
        self.deleted_order_id = uuid4()
        self.closed_product_quantity_id = uuid4()
        self.closed_order_id = uuid4()
        self.new_product_id = uuid4()
        self.order_id = uuid4()
        self.product_id = uuid4()
        self.product_quantity_id = uuid4()
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

        self.new_product = Product.objects.create(
            id=self.new_product_id,
            name="test_product_name_new",
            description="test_product_description",
            price=100,
        )

        self.order = Order.objects.create(
            id=self.order_id,
            external_client="test_external_client",
            total_price=100,
        )

        self.deleted_order = Order.objects.create(
            id=self.deleted_order_id,
            external_client="test_external_client",
            total_price=100,
            deleted_at=now(),
        )

        self.closed_order = Order.objects.create(
            id=self.closed_order_id,
            external_client="test_external_client",
            total_price=100,
            closed_at=now(),
        )

        self.closed_product_quantity = ProductQuantity.objects.create(
            id=self.closed_product_quantity_id,
            product_id=self.product_id,
            order_id=self.closed_order_id,
            quantity=10,
        )

        self.deleted_product_quantity = ProductQuantity.objects.create(
            id=self.deleted_product_quantity_id,
            product_id=self.deleted_product_id,
            order_id=self.deleted_order_id,
            quantity=10,
            deleted_at=now(),
        )

        self.product_quantity = ProductQuantity.objects.create(
            id=self.product_quantity_id,
            product_id=self.product_id,
            order_id=self.order_id,
            quantity=10,
        )

    def test_product_quantity_post(self):
        """
        Tests the POST method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities",
            kwargs={"order_id": self.order_id},
        )

        request_payload = {
            "product": {"id": self.new_product_id},
            "quantity": 10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload, format="json")

        # assert
        assert response.status_code == 201
        assert response.data.get("quantity") == request_payload.get("quantity")

    def test_product_quantity_post_unprocessable_entity_when_product_not_found(self):
        """
        Tests the POST method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities",
            kwargs={"order_id": self.order_id},
        )

        request_payload = {
            "product": {"id": uuid4()},
            "quantity": 10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload, format="json")

        # assert
        assert response.status_code == 404

    def test_product_quantity_post_unprocessable_entity_when_product_already_registered(
        self,
    ):
        """
        Tests the POST method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities",
            kwargs={"order_id": self.order_id},
        )

        request_payload = {
            "product": {"id": self.product_id},
            "quantity": 10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload, format="json")

        # assert
        assert response.status_code == 422

    def test_product_quantity_post_unprocessable_entity_when_order_is_closed(self):
        """
        Tests the POST method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities",
            kwargs={"order_id": self.closed_order_id},
        )

        request_payload = {
            "product": {"id": self.new_product_id},
            "quantity": 10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload, format="json")

        # assert
        assert response.status_code == 422

    def test_product_quantity_post_unprocessable_entity_when_order_does_not_exist(self):
        """
        Tests the POST method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities",
            kwargs={"order_id": uuid4()},
        )

        request_payload = {
            "product": {"id": self.new_product_id},
            "quantity": 10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload, format="json")

        # assert
        assert response.status_code == 404

    def test_product_quantity_post_unprocessable_entity_when_order_logical_deleted(
        self,
    ):
        """
        Tests the POST method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities",
            kwargs={"order_id": self.deleted_order_id},
        )

        request_payload = {
            "product": {"id": self.new_product_id},
            "quantity": 10,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload, format="json")

        # assert
        assert response.status_code == 404

    def test_product_quantity_post_bad_request(
        self,
    ):
        """
        Tests the POST method of product quantity view.
        """
        # arrange
        self.setup()
        url = reverse(
            "orders_product_quantities",
            kwargs={"order_id": self.deleted_order_id},
        )

        request_payload = {
            "product": {"id": self.new_product_id},
            "quantity": "hello",
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_payload, format="json")

        # assert
        assert response.status_code == 400
