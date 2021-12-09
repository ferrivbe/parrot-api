"""
File name: urls.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from django.urls import path

from api.views.order_view import OrderView
from api.views.product_view import ProductByIdView, ProductView

urlpatterns = [
    # Product endpoints.
    path("products", ProductView.as_view(), name="products"),
    path("products/<uuid:id>", ProductByIdView.as_view(), name="products_id"),
    # Order endpoints.
    path("orders", OrderView.as_view(), name="orders"),
]
