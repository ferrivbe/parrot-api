"""
File name: product_quantity_serializer.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework.serializers import ModelSerializer

from api.models.product_quantity import ProductQuantity
from api.serializers.product_serializer import ProductSerializer


class ProductQuantitySerializer(ModelSerializer):
    """
    The product quantity serializer.
    """

    product = ProductSerializer(required=True, many=False)

    class Meta:
        model = ProductQuantity
        fields = [
            "product",
            "quantity",
        ]
        depth = 2
