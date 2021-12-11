"""
File name: product_report_view.py
Author: Fernando Rivera
Creation date: 2021-12-10
"""
from datetime import datetime
from utils.configurations.constants import GenericConstants, ExceptionConstants
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from api.serializers.responses.product_report_response_serializer import (
    ProductReportResponseSerializer,
)
from api.services.product_quantity_service import ProductQuantityService
from utils.exceptions.serializers.api_exception_serializer import ApiExceptionSerializer
from utils.validations.api_validations import ApiValidations
from utils.exceptions.api_exceptions import BadRequestException


class ProductReportView(APIView):
    """
    The product report view.

    Manage requests for product reports.
    """

    def __init__(self):
        """
        Creates a new instance of ProductReportView.
        """
        self.permission_classes = (permissions.IsAuthenticated,)
        self.service = ProductQuantityService()
        self.validator = ApiValidations()

    @swagger_auto_schema(
        operation_description="Gets a product by identifier.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                "The order closure start date.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                "The order closure end date.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
            ),
        ],
        responses={
            200: openapi.Response(
                "Product report found.", ProductReportResponseSerializer()
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
    def get(self, request, format=None):
        """
        Gets the product report.

        :param rest_framework.request request: The HTTP request.
        :param uuid4 id: The product identifier.
        """
        start_date = self.validator.validate_date(
            request.GET.get(GenericConstants.START_DATE)
        )
        end_date = self.validator.validate_date(
            request.GET.get(GenericConstants.END_DATE)
        )

        product_report = self.service.get_product_quantity_by_order_closure_date(
            start_date,
            end_date,
        )

        return Response(product_report, status=status.HTTP_200_OK)
