"""
File name: product_quantity_view.py
Author: Fernando Rivera
Creation date: 2021-12-09
"""
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from api.serializers.product_quantity_serializer import (
    ProductQuantityCreateSerializer,
    ProductQuantityUpdateSerializer,
)
from api.serializers.responses.product_quantity_response_serializer import (
    ProductQuantityResponseSerializer,
)
from api.services.product_quantity_service import ProductQuantityService
from utils.exceptions.api_exceptions import BadRequestException
from utils.exceptions.serializers.api_exception_serializer import ApiExceptionSerializer
from utils.validations.api_validations import ApiValidations


class ProductQuantityByIdView(APIView):
    """
    The product quantity by identifier view.

    Manage requests for product_quantity objects by identifier.
    """

    def __init__(self):
        """
        Creates a new instance of ProductQuantityByIdView.
        """
        self.permission_classes = (permissions.IsAuthenticated,)
        self.serializer = ProductQuantityUpdateSerializer
        self.service = ProductQuantityService()
        self.validator = ApiValidations()

    @swagger_auto_schema(
        operation_description="Deletes a product quantity by identifier.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "order_id",
                openapi.IN_PATH,
                "The order identifier.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "The product quantity identifier.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            ),
        ],
        responses={
            200: openapi.Response(
                "Product quantity deleted.", ProductQuantityResponseSerializer()
            ),
            401: openapi.Response(
                "User not authorized.", ApiExceptionSerializer(many=False)
            ),
            404: openapi.Response("Not found.", ApiExceptionSerializer(many=False)),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def delete(self, request, order_id, id, format=None):
        """
        Deletes the product by identifier.

        :param rest_framework.request request: The HTTP request.
        :param order_id uuid4: The product identifier.
        :param uuid4 id: The product identifier.
        """
        product_quantity = self.service.delete_product_quantity_by_id(order_id, id)

        return Response(product_quantity.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Gets a product quantity by identifier.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "order_id",
                openapi.IN_PATH,
                "The order identifier.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "The product quantity identifier.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            ),
        ],
        responses={
            200: openapi.Response(
                "Product quantity found.", ProductQuantityResponseSerializer()
            ),
            401: openapi.Response(
                "User not authorized.", ApiExceptionSerializer(many=False)
            ),
            404: openapi.Response("Not found.", ApiExceptionSerializer(many=False)),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def get(self, request, order_id, id, format=None):
        """
        Gets the product by identifier.

        :param rest_framework.request request: The HTTP request.
        :param order_id uuid4: The product identifier.
        :param uuid4 id: The product identifier.
        """
        product_quantity = self.service.get_product_quantity_by_id(order_id, id)

        return Response(product_quantity.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Updates a product quantity by identifier.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "order_id",
                openapi.IN_PATH,
                "The order identifier.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "The product quantity identifier.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            ),
        ],
        request_body=ProductQuantityUpdateSerializer(),
        responses={
            200: openapi.Response(
                "Product quantity updated.", ProductQuantityResponseSerializer()
            ),
            401: openapi.Response(
                "User not authorized.", ApiExceptionSerializer(many=False)
            ),
            404: openapi.Response("Not found.", ApiExceptionSerializer(many=False)),
            422: openapi.Response(
                "Unprocessable entity exception", ApiExceptionSerializer(many=False)
            ),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def put(self, request, order_id, id, format=None):
        """
        Updates the product by identifier.

        :param rest_framework.request request: The HTTP request.
        :param order_id uuid4: The product identifier.
        :param uuid4 id: The product identifier.
        """
        self.validator.is_null(request)
        request_serializer = self.serializer(data=request.data)

        if request_serializer.is_valid():
            product_created = self.service.update_product_quantity_by_id(
                request_serializer.data,
                order_id,
                id,
            )

            return Response(product_created.data, status=status.HTTP_200_OK)

        raise BadRequestException(request_serializer.errors)


class ProductQuantityView(APIView):
    """
    The product quantity view.

    Manage requests for product_quantity objects.
    """

    def __init__(self):
        """
        Creates a new instance of ProductQuantityView.
        """
        self.permission_classes = (permissions.IsAuthenticated,)
        self.serializer = ProductQuantityCreateSerializer
        self.service = ProductQuantityService()
        self.validator = ApiValidations()

    @swagger_auto_schema(
        operation_description="Creates a product quantity.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "order_id",
                openapi.IN_PATH,
                "The order identifier.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            ),
        ],
        request_body=ProductQuantityCreateSerializer(),
        responses={
            200: openapi.Response(
                "Product quantity updated.", ProductQuantityResponseSerializer()
            ),
            401: openapi.Response(
                "User not authorized.", ApiExceptionSerializer(many=False)
            ),
            422: openapi.Response(
                "Unprocessable entity exception", ApiExceptionSerializer(many=False)
            ),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def post(self, request, order_id, format=None):
        """
        Creates the product by identifier.

        :param rest_framework.request request: The HTTP request.
        :param order_id uuid4: The product identifier.
        """
        self.validator.is_null(request)
        request_serializer = self.serializer(data=request.data)

        if request_serializer.is_valid():
            product_created = self.service.create_product_quantity(
                request_serializer.data,
                order_id,
            )

            return Response(product_created.data, status=status.HTTP_201_CREATED)

        raise BadRequestException(request_serializer.errors)
