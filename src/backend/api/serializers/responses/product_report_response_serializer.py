"""
File name: product_report_response_serializer.py
Author: Fernando Rivera
Creation date: 2021-12-10
"""
from rest_framework import serializers


class ProductReportResponseSerializer(serializers.Serializer):
    """
    The product report response serializer.
    """

    id = serializers.UUIDField(read_only=True)
    """
    The product identifier.
    """

    name = serializers.CharField(read_only=True)
    """
    The prodcut name.
    """

    description = serializers.CharField(read_only=True)
    """
    The product description.
    """

    total_quantity = serializers.IntegerField(read_only=True)
    """
    The product total sold quantity.
    """

    total_price = serializers.IntegerField(read_only=True)
    """
    The product total sold price.
    """
