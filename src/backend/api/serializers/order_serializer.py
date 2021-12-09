"""
File name: order_serializer.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework.serializers import ModelSerializer

from api.models.order import Order
from api.serializers.product_quantity_serializer import ProductQuentitySerializer


class OrderSerializer(ModelSerializer):
    """
    The order serializer.
    """

    product_quantities = ProductQuentitySerializer(required=True, many=False)

    class Meta:
        model = Order
        fields = [
            "external_client",
            "total_price",
            "product_quantities",
        ]
        depth = 1
