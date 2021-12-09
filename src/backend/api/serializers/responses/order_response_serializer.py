"""
File name: order_response_serializer.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework.serializers import ModelSerializer

from api.models.order import Order
from api.serializers.responses.product_quantity_response_serializer import (
    ProductQuentityResponseSerializer,
)


class OrderResponseSerializer(ModelSerializer):
    """
    The order response serializer.
    """

    product_quantities = ProductQuentityResponseSerializer(required=True, many=True)

    class Meta:
        model = Order
        fields = [
            "external_client",
            "total_price",
            "product_quantities",
        ]
        depth = 1
