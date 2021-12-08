"""
File name: product_response_serializer.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from rest_framework.serializers import ModelSerializer

from api.models.product import Product


class ProductResponseSerializer(ModelSerializer):
    """
    The product response serializer.
    """

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
        ]
        depth = 1
