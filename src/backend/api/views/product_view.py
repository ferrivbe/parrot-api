"""
File name: product_view.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from api.serializers.product_serializer import ProductSerializer
from api.serializers.responses.product_response_serializer import (
    ProductResponseSerializer,
)
from api.services.product_service import ProductService
from utils.exceptions.api_exceptions import BadRequestException
from utils.exceptions.serializers.api_exception_serializer import ApiExceptionSerializer
from utils.validations.api_validations import ApiValidations


class ProductByIdView(APIView):
    """
    The product by identifier view.

    Manage requests for product objects by identifier.
    """

    def __init__(self):
        """
        Creates a new instance of ProductByIdView
        """
        self.permission_classes = (permissions.AllowAny,)
        self.serializer = ProductSerializer
        self.service = ProductService()
        self.validator = ApiValidations()

    @swagger_auto_schema(
        operation_description="Deletes a product by identifier.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type="string",
            ),
            openapi.Parameter(
                "id", openapi.IN_PATH, "The product identifier.", type="uuid4"
            ),
        ],
        responses={
            200: openapi.Response("Product deleted.", ProductResponseSerializer()),
            404: openapi.Response("Not found.", ApiExceptionSerializer(many=False)),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def delete(self, request, id, format=None):
        """
        Deletes the product by identifier.

        :param rest_framework.request request: The HTTP request.
        :param id uuid4: The product identifier.
        """
        product = self.service.delete_product_by_id(id)

        return Response(product.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Gets a product by identifier.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type="string",
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "The product identifier.",
                type="uuid4",
            ),
        ],
        responses={
            200: openapi.Response("Product found.", ProductResponseSerializer()),
            404: openapi.Response("Not found.", ApiExceptionSerializer(many=False)),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def get(self, request, id, format=None):
        """
        Gets the product by identifier.

        :param rest_framework.request request: The HTTP request.
        :param id uuid4: The product identifier.
        """
        product = self.service.get_product_by_id(id)

        return Response(product.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Updates a product by identifier.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type="string",
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "The product identifier.",
                type="uuid4",
            ),
        ],
        responses={
            200: openapi.Response("Product found.", ProductResponseSerializer()),
            404: openapi.Response("Not found.", ApiExceptionSerializer(many=False)),
            422: openapi.Response(
                "Resuest has errors", ApiExceptionSerializer(many=False)
            ),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def put(self, request, id, format=None):
        """
        Updates the product by identifier.

        :param rest_framework.request request: The HTTP request.
        :param id uuid4: The product identifier.
        """
        self.validator.is_null(request)
        request_serializer = self.serializer(data=request.data)

        if request_serializer.is_valid():
            product_created = self.service.update_product(request_serializer.data, id)

            return Response(product_created.data, status=status.HTTP_200_OK)

        raise BadRequestException(request_serializer.errors)


class ProductView(APIView):
    """
    The product view.

    Manage requests for product objects.
    """

    def __init__(self):
        """
        Creates a new instance of ProductView.
        """
        self.permission_classes = (permissions.AllowAny,)
        self.serializer = ProductSerializer
        self.service = ProductService()
        self.validator = ApiValidations()

    @swagger_auto_schema(
        operation_description="Creates a product.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type="string",
            )
        ],
        request_body=ProductSerializer(),
        responses={
            201: openapi.Response("Product created.", ProductResponseSerializer()),
            404: openapi.Response("Not found.", ApiExceptionSerializer(many=False)),
            422: openapi.Response("Bad request.", ApiExceptionSerializer(many=False)),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def post(self, request, format=None):
        """
        Creates the product.

        :param rest_framework.request request: The request.
        :param uuid id: The menu identifier.
        """
        self.validator.is_null(request)
        request_serializer = self.serializer(data=request.data)

        if request_serializer.is_valid():
            product_created = self.service.create_product(request_serializer.data)

            return Response(product_created.data, status=status.HTTP_201_CREATED)

        raise BadRequestException(request_serializer.errors)
