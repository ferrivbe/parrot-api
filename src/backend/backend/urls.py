"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from backend.utils.health import HealthView

schema_view = get_schema_view(
    openapi.Info(
        title="Parrot API",
        default_version="v1",
        description="Backend Coding Challenge.",
        contact=openapi.Contact(email="fernando.rivbe@icloud.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # api
    path("", include("api.urls")),
    # user
    path("users", include("auth_api.urls")),
    # health
    path("health", HealthView.as_view(), name="health"),
    # docs
    path(
        "swagger",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    # authentication
    path("auth/tokens", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/tokens/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/tokens/verify", TokenVerifyView.as_view(), name="token_verify"),
]
