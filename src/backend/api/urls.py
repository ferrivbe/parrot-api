"""
File name: urls.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from django.urls import path

from api.views.order_view import OrderByIdView, OrderClosureView, OrderView
from api.views.product_quantity_view import ProductQuantityByIdView, ProductQuantityView
from api.views.product_report_view import ProductReportView
from api.views.product_view import ProductByIdView, ProductView

urlpatterns = [
    # Product endpoints.
    path(
        "products",
        ProductView.as_view(),
        name="products",
    ),
    path(
        "products/<uuid:id>",
        ProductByIdView.as_view(),
        name="products_id",
    ),
    # Order endpoints.
    path(
        "orders",
        OrderView.as_view(),
        name="orders",
    ),
    path(
        "orders/<uuid:id>",
        OrderByIdView.as_view(),
        name="orders_id",
    ),
    path(
        "orders/<uuid:id>/closures",
        OrderClosureView.as_view(),
        name="orders_id_closures",
    ),
    # Product quantity endpoints.
    path(
        "orders/<uuid:order_id>/product-quantities",
        ProductQuantityView.as_view(),
        name="orders_product_quantities",
    ),
    path(
        "orders/<uuid:order_id>/product-quantities/<uuid:id>",
        ProductQuantityByIdView.as_view(),
        name="orders_product_quantities_id",
    ),
    # Prodcut report endpoints.
    path(
        "products/reports",
        ProductReportView.as_view(),
        name="products_reports",
    ),
]
