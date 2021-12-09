"""
File name: urls.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from django.urls import path

from auth_api.views.user_view import UserLoginView, UserView

urlpatterns = [
    path("", UserView.as_view(), name="users"),
    path("/login", UserLoginView.as_view(), name="users-login"),
]
