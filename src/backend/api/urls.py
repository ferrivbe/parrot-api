"""
File name: urls.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from django.urls import path

from api.views import product_view

urlpatterns = [
    # Product endpoints.
    path("products", product_view.ProductView.as_view(), name="products"),
    path(
        "products/<uuid:id>", product_view.ProductByIdView.as_view(), name="products_id"
    ),
]
