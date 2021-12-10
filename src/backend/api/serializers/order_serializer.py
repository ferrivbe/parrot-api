"""
File name: order_serializer.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework.serializers import ModelSerializer

from api.models.order import Order
from api.serializers.product_quantity_serializer import ProductQuantitySerializer


class OrderSerializer(ModelSerializer):
    """
    The order serializer.
    """

    product_quantities = ProductQuantitySerializer(required=True, many=True)

    class Meta:
        model = Order
        fields = [
            "external_client",
            "product_quantities",
        ]
        depth = 1


class OrderUpdateSerializer(ModelSerializer):
    """
    The order update serializer.
    """

    class Meta:
        model = Order
        fields = [
            "external_client",
        ]
