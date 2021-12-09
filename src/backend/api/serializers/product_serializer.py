"""
File name: product_serializer.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from rest_framework.serializers import ModelSerializer

from api.models.product import Product


class ProductSerializer(ModelSerializer):
    """
    The product serializer.
    """

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
        ]
        depth = 1
