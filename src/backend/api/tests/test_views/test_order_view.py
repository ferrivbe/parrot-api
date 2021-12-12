"""
File name: test_order_view.py
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


class TestOrderByIdView(APITestCase):
    """
    The test order by identifier view class.

    Tests the OrderByIdView class.
    """

    def setup(self):
        """
        TestOrderByIdView class setup.
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

    def test_order_by_id_get(self):
        """
        Tests the GET method order by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id", kwargs={"id": self.order_id})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # assert
        assert response.status_code == 200
        assert response.data.get("id") == str(self.order_id)

    def test_order_by_id_get_not_found(self):
        """
        Tests the GET method order by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id", kwargs={"id": uuid4()})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # assert
        assert response.status_code == 404

    def test_order_by_id_get_not_found_when_logical_delete(self):
        """
        Tests the GET method order by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id", kwargs={"id": self.deleted_order_id})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # assert
        assert response.status_code == 404

    def test_order_by_id_delete(self):
        """
        Tests the DELETE method order by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id", kwargs={"id": self.order_id})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # assert
        assert response.status_code == 200
        assert response.data.get("id") == str(self.order_id)

    def test_order_by_id_delete_not_found(self):
        """
        Tests the DELETE method order by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id", kwargs={"id": uuid4()})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # assert
        assert response.status_code == 404

    def test_order_by_id_delete_when_logical_delete(self):
        """
        Tests the DELETE method order by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id", kwargs={"id": self.deleted_order_id})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # assert
        assert response.status_code == 404

    def test_order_by_id_put(self):
        """
        Tests the PUT method order by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id", kwargs={"id": self.order_id})
        request_payload = {"external_client": "test_subject"}

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload, format="json")

        # assert
        assert response.status_code == 200
        assert response.data.get("external_client") == "test_subject"

    def test_order_by_id_put_not_found(self):
        """
        Tests the PUT method order by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id", kwargs={"id": uuid4()})
        request_payload = {"external_client": "test_subject"}

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload, format="json")

        # assert
        assert response.status_code == 404

    def test_order_by_id_put_not_found_when_logical_delete(self):
        """
        Tests the PUT method order by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id", kwargs={"id": self.deleted_order_id})
        request_payload = {"external_client": "test_subject"}

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload, format="json")

        # assert
        assert response.status_code == 404

    def test_order_by_id_put_bad_request(self):
        """
        Tests the PUT method order by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id", kwargs={"id": self.order_id})
        request_payload = {"external_client": "test_subject !"}

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload, format="json")

        # assert
        assert response.status_code == 400

    def test_order_by_id_put_unprocessable_entity_when_closed_order(self):
        """
        Tests the PUT method order by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id", kwargs={"id": self.closed_order_id})
        request_payload = {"external_client": "test_subject"}

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload, format="json")

        # assert
        assert response.status_code == 422

    def test_order_by_id_put_unprocessable_entity_when_missing_parameter(self):
        """
        Tests the PUT method order by identifier view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id", kwargs={"id": self.closed_order_id})
        request_payload = {"external_client": None}

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, request_payload, format="json")

        # assert
        assert response.status_code == 422


class TestOrderView(APITestCase):
    """
    The test order view class.

    Tests the OrderView class.
    """

    def setup(self):
        """
        TestOrderView class setup.
        """
        self.product_id = uuid4()
        self.deleted_product_id = uuid4()

        self.user_id = uuid4()

        self.user = User.objects.create(
            id=self.user_id,
            email="test@test.com",
            password="test",
            first_name="test_name",
            last_name="test_last_name",
            role=2,
        )

        Product.objects.create(
            id=self.product_id,
            name="test_product_name",
            description="test_product_description",
            price=100,
        )
        Product.objects.create(
            id=self.deleted_product_id,
            name="deleted_test_product_name",
            description="test_product_description",
            price=110,
            deleted_at=now(),
        )

    def test_order_post(self):
        """
        Tests the POST method order view.
        """
        # arrange
        self.setup()
        url = reverse("orders")
        request_data = {
            "external_client": "external_client",
            "total_price": 158400,
            "product_quantities": [
                {
                    "product": {
                        "name": "mole",
                        "description": "A mole",
                        "price": 55900,
                    },
                    "quantity": 3,
                },
                {
                    "product": {
                        "name": "banana",
                        "description": "A banana",
                        "price": 2500,
                    },
                    "quantity": 1,
                },
                {
                    "product": {
                        "name": "banana",
                        "description": "A banana",
                        "price": 2500,
                    },
                    "quantity": 10,
                },
            ],
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_data, format="json")

        # assert
        assert response.status_code == 201
        assert response.data.get("external_client") == "external_client"

    def test_order_post_ok_when_product_exists(self):
        """
        Tests the POST method order view.
        """
        # arrange
        self.setup()
        url = reverse("orders")
        request_data = {
            "external_client": "external_client",
            "total_price": 158400,
            "product_quantities": [
                {
                    "product": {
                        "name": "test_product_name",
                        "description": "test_product_description",
                        "price": 55900,
                    },
                    "quantity": 3,
                },
                {
                    "product": {
                        "name": "banana",
                        "description": "A banana",
                        "price": 2500,
                    },
                    "quantity": 1,
                },
                {
                    "product": {
                        "name": "banana",
                        "description": "A banana",
                        "price": 2500,
                    },
                    "quantity": 10,
                },
            ],
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_data, format="json")

        # assert
        assert response.status_code == 201
        assert response.data.get("external_client") == "external_client"

    def test_order_post_bad_request(self):
        """
        Tests the POST method order view.
        """
        # arrange
        self.setup()
        url = reverse("orders")
        request_data = {
            "external_client": "external_client",
            "total_price": 158400,
            "product_quantities": "hello !",
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_data, format="json")

        # assert
        assert response.status_code == 400

    def test_order_post_bad_request_when_parameter_is_missing(self):
        """
        Tests the POST method order view.
        """
        # arrange
        self.setup()
        url = reverse("orders")
        request_data = {
            "external_client": "external_client",
            "total_price": 158400,
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_data, format="json")

        # assert
        assert response.status_code == 400

    def test_order_post_unprocessable_entity_when_quantities_zero(self):
        """
        Tests the POST method order view.
        """
        # arrange
        self.setup()
        url = reverse("orders")
        request_data = {
            "external_client": "external_client",
            "total_price": 158400,
            "product_quantities": [
                {
                    "product": {
                        "name": "test_product_name",
                        "description": "test_product_description",
                        "price": 55900,
                    },
                    "quantity": 0,
                },
                {
                    "product": {
                        "name": "banana",
                        "description": "A banana",
                        "price": 2500,
                    },
                    "quantity": 1,
                },
                {
                    "product": {
                        "name": "banana",
                        "description": "A banana",
                        "price": 2500,
                    },
                    "quantity": 10,
                },
            ],
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_data, format="json")

        # assert
        assert response.status_code == 422

    def test_order_post_unprocessable_entity_when_quantities_negative(self):
        """
        Tests the POST method order view.
        """
        # arrange
        self.setup()
        url = reverse("orders")
        request_data = {
            "external_client": "external_client",
            "total_price": 158400,
            "product_quantities": [
                {
                    "product": {
                        "name": "test_product_name",
                        "description": "test_product_description",
                        "price": 55900,
                    },
                    "quantity": -10,
                },
                {
                    "product": {
                        "name": "banana",
                        "description": "A banana",
                        "price": 2500,
                    },
                    "quantity": 1,
                },
                {
                    "product": {
                        "name": "banana",
                        "description": "A banana",
                        "price": 2500,
                    },
                    "quantity": 10,
                },
            ],
        }

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, request_data, format="json")

        # assert
        assert response.status_code == 422


class TestOrderClosuresView(APITestCase):
    """
    The test order closures view class.

    Tests the OrderClosuresView class.
    """

    def setup(self):
        """
        TestOrderClosuresView class setup.
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

    def test_order_closure_patch(self):
        """
        Tests the PATCH method order closure view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id_closures", kwargs={"id": self.order_id})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url)

        # assert
        assert response.status_code == 200
        assert response.data.get("closed_at") is not None

    def test_order_closure_patch_not_found(self):
        """
        Tests the PATCH method order closure view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id_closures", kwargs={"id": uuid4()})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url)

        # assert
        assert response.status_code == 404

    def test_order_closure_patch_not_found_when_locial_delete(self):
        """
        Tests the PATCH method order closure view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id_closures", kwargs={"id": self.deleted_order_id})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url)

        # assert
        assert response.status_code == 404

    def test_order_closure_patch_unprocessable_entity_when_closed_order(self):
        """
        Tests the PATCH method order closure view.
        """
        # arrange
        self.setup()
        url = reverse("orders_id_closures", kwargs={"id": self.closed_order_id})

        # act
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url)

        # assert
        assert response.status_code == 422
