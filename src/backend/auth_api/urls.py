"""
File name: urls.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from auth_api.views.user_view import UserLoginView, UserView

urlpatterns = [
    # User endpoints
    path("", UserView.as_view(), name="users"),
    path("/login", UserLoginView.as_view(), name="users-login"),
    # Authentication
    path("/tokens/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("/tokens/verify", TokenVerifyView.as_view(), name="token_verify"),
]
