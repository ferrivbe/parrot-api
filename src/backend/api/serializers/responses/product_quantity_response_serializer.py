"""
File name: product_quantity_serializer.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework.serializers import ModelSerializer

from api.models.product_quantity import ProductQuantity
from api.serializers.responses.product_response_serializer import (
    ProductResponseSerializer,
)


class ProductQuentityResponseSerializer(ModelSerializer):
    """
    The product quantity response serializer.
    """

    product = ProductResponseSerializer(required=True, many=False)

    class Meta:
        model = ProductQuantity
        fields = [
            "id",
            "product",
            "quantity",
        ]
        depth = 1
