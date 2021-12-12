"""
File name: order_view.py
Author: Fernando Rivera
Creation date: 2021-12-09
"""
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from api.serializers.order_serializer import OrderSerializer, OrderUpdateSerializer
from api.serializers.responses.order_response_serializer import OrderResponseSerializer
from api.services.order_service import OrderService
from utils.exceptions.api_exceptions import BadRequestException
from utils.exceptions.serializers.api_exception_serializer import ApiExceptionSerializer
from utils.validations.api_validations import ApiValidations


class OrderByIdView(APIView):
    """
    The order by identifier view.

    Manage requests for order objects.
    """

    def __init__(self):
        """
        Creates a new instance of OrderByIdView.
        """
        self.permission_classes = (permissions.IsAuthenticated,)
        self.serializer = OrderUpdateSerializer
        self.service = OrderService()
        self.validator = ApiValidations()

    @swagger_auto_schema(
        operation_description="Deletes an order.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "The order identifier.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            ),
        ],
        responses={
            200: openapi.Response("Order deleted.", OrderResponseSerializer()),
            401: openapi.Response(
                "User not authorized.", ApiExceptionSerializer(many=False)
            ),
            404: openapi.Response("Not found", ApiExceptionSerializer(many=False)),
            422: openapi.Response("Bad request.", ApiExceptionSerializer(many=False)),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def delete(self, request, id, format=None):
        """
        Deletes the order.

        :param rest_framework.request request: The request.
        :param uuid id: The order identifier.
        """
        order = self.service.delete_order_by_id(id)

        return Response(order.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Gets an order.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "The order identifier.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            ),
        ],
        responses={
            200: openapi.Response("Order found.", OrderResponseSerializer()),
            401: openapi.Response(
                "User not authorized.", ApiExceptionSerializer(many=False)
            ),
            404: openapi.Response("Not found", ApiExceptionSerializer(many=False)),
            422: openapi.Response("Bad request.", ApiExceptionSerializer(many=False)),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def get(self, request, id, format=None):
        """
        Gets the order.

        :param rest_framework.request request: The request.
        :param uuid id: The order identifier.
        """
        order = self.service.get_order_by_id(id)

        return Response(order.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Upates an order.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "The order identifier.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            ),
        ],
        request_body=OrderUpdateSerializer(),
        responses={
            200: openapi.Response("Order updated.", OrderResponseSerializer()),
            401: openapi.Response(
                "User not authorized.", ApiExceptionSerializer(many=False)
            ),
            404: openapi.Response("Not found", ApiExceptionSerializer(many=False)),
            422: openapi.Response("Bad request.", ApiExceptionSerializer(many=False)),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def put(self, request, id, format=None):
        """
        Updates the order.

        :param rest_framework.request request: The request.
        :param uuid id: The order identifier.
        """
        self.validator.is_null(request)
        request_serializer = self.serializer(data=request.data)

        if request_serializer.is_valid():
            order_updated = self.service.update_order_by_id(request_serializer.data, id)

            return Response(order_updated.data, status=status.HTTP_200_OK)

        raise BadRequestException(request_serializer.errors)


class OrderClosureView(APIView):
    """
    The order closure view.

    Manage requests for order objects, in closed_at parameter.
    """

    def __init__(self):
        """
        Creates a new instance of OrderClosureView.
        """
        self.permission_classes = (permissions.IsAuthenticated,)
        self.service = OrderService()

    @swagger_auto_schema(
        operation_description="Patches an order closure.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "The order identifier.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            ),
        ],
        responses={
            201: openapi.Response("Order closed.", OrderResponseSerializer()),
            401: openapi.Response(
                "User not authorized.", ApiExceptionSerializer(many=False)
            ),
            404: openapi.Response("Not found", ApiExceptionSerializer(many=False)),
            422: openapi.Response("Bad request.", ApiExceptionSerializer(many=False)),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def patch(self, request, id, format=None):
        """
        Creates the order.

        :param rest_framework.request request: The request.
        """
        order = self.service.update_order_closure(id)

        return Response(order.data, status=status.HTTP_200_OK)


class OrderView(APIView):
    """
    The order view.

    Manage requests for order objects.
    """

    def __init__(self):
        """
        Creates a new instance of OrderView.
        """
        self.permission_classes = (permissions.IsAuthenticated,)
        self.serializer = OrderSerializer
        self.service = OrderService()
        self.validator = ApiValidations()

    @swagger_auto_schema(
        operation_description="Creates an order.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type=openapi.TYPE_STRING,
            )
        ],
        request_body=OrderSerializer(),
        responses={
            201: openapi.Response("Order created.", OrderResponseSerializer()),
            401: openapi.Response(
                "User not authorized.", ApiExceptionSerializer(many=False)
            ),
            422: openapi.Response("Bad request.", ApiExceptionSerializer(many=False)),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def post(self, request, format=None):
        """
        Creates the order.

        :param rest_framework.request request: The request.
        """
        self.validator.is_null(request)
        request_serializer = self.serializer(data=request.data)

        if request_serializer.is_valid():
            ordert_created = self.service.create_order(request_serializer.data)

            return Response(ordert_created.data, status=status.HTTP_201_CREATED)

        raise BadRequestException(request_serializer.errors)
