"""
File name: user_view.py
Author: Fernando Rivera
Creation date: 2021-12-08
"""
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from auth_api.serializers import user_list, user_login, user_password, user_registration
from auth_api.services.user_service import UserService
from utils.configurations.constants import ExceptionConstants, GenericConstants
from utils.exceptions.api_exceptions import (
    BadRequestException,
    ForbiddenEntityException,
)
from utils.exceptions.serializers.api_exception_serializer import ApiExceptionSerializer


class UserView(APIView):
    """
    The user view.
    """

    def __init__(self):
        """
        Creates a new instance of UserView.
        """
        self.password_serializer = user_password.UserPasswordSerializer
        self.permission_classes = (IsAuthenticated,)
        self.register_serializer = user_registration.UserRegistrationSerializer
        self.serializer = user_list.UserListSerializer
        self.user_service = UserService()

    @swagger_auto_schema(
        operation_description="Gets users.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type="string",
            ),
        ],
        responses={
            200: openapi.Response(
                "User found.", user_list.UserListSerializer(many=False)
            ),
            400: openapi.Response("Bad request.", ApiExceptionSerializer(many=False)),
            404: openapi.Response(
                "User not found.", ApiExceptionSerializer(many=False)
            ),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def get(self, request):
        """
        Gets the list of registered users.
        """

        user = request.user
        user_found = self.user_service.get_user(user.id)
        return Response(user_found, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Creates a user.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type="string",
            ),
        ],
        responses={
            200: openapi.Response(
                "User deleted.", user_list.UserListSerializer(many=False)
            ),
            400: openapi.Response("Bad request.", ApiExceptionSerializer(many=False)),
            404: openapi.Response(
                "User not found.", ApiExceptionSerializer(many=False)
            ),
            422: openapi.Response(
                "Unprocessable entity.", ApiExceptionSerializer(many=False)
            ),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def delete(self, request):
        """
        Updates the user resource fully.
        """
        user = request.user
        user_deleted = self.user_service.delete_user(user.id)
        return Response(user_deleted, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Creates a user.",
        request_body=user_registration.UserRegistrationSerializer(),
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type="string",
            ),
        ],
        responses={
            201: openapi.Response(
                "User created.", user_list.UserListSerializer(many=False)
            ),
            400: openapi.Response("Bad request.", ApiExceptionSerializer(many=False)),
            422: openapi.Response(
                "Unprocessable entity.", ApiExceptionSerializer(many=False)
            ),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def post(self, request, format=None):
        """
        Creates a user.

        :param rest_framework.request request: The request.
        """
        creator_role = request.user.role
        serializer = self.register_serializer(data=request.data)

        if serializer.is_valid():
            user_role = int(serializer.validated_data.get("role"))
            self.validate_role(creator_role, user_role)
            user = self.user_service.create_user(serializer)

            return Response(user, status=status.HTTP_201_CREATED)

        raise BadRequestException(serializer.errors)

    @swagger_auto_schema(
        operation_description="Updates a user password.",
        request_body=user_password.UserPasswordSerializer(),
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                "The user authorization.",
                type="string",
            ),
        ],
        responses={
            201: openapi.Response(
                "User created.", user_list.UserListSerializer(many=False)
            ),
            400: openapi.Response("Bad request.", ApiExceptionSerializer(many=False)),
            422: openapi.Response(
                "Unprocessable entity.", ApiExceptionSerializer(many=False)
            ),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def patch(self, request, format=None):
        """
        Creates a user.

        :param rest_framework.request request: The request.
        """
        id = request.user.id
        serializer = self.password_serializer(data=request.data)

        if serializer.is_valid():
            user = self.user_service.update_password(serializer, id)

            return Response(user, status=status.HTTP_200_OK)

        raise BadRequestException(serializer.errors)

    def validate_role(self, creator_role, user_role):
        """
        Validates if creator can create user with role.

        :param int creator_role: The creator role.
        :param int user_role: The user role.
        """
        if user_role <= creator_role:
            raise ForbiddenEntityException(
                ExceptionConstants.USER_CREATION_ROLE_NOT_VALID
                % {
                    GenericConstants.CREATOR_ROLE: creator_role,
                    GenericConstants.USER_ROLE: user_role,
                }
            )


class UserLoginView(APIView):
    """
    The user login view.
    """

    def __init__(self):
        """
        Creates a new instance of UserLoginView.
        """
        self.seralizer = user_login.UserLoginSerializer
        self.service = UserService()
        self.permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Authenticate user.",
        request_body=user_login.UserLoginSerializer(),
        responses={
            200: openapi.Response("User authenticated."),
            400: openapi.Response("Bad request.", ApiExceptionSerializer(many=False)),
            422: openapi.Response(
                "Unprocessable entity.", ApiExceptionSerializer(many=False)
            ),
            500: openapi.Response(
                "Internal server error.", ApiExceptionSerializer(many=False)
            ),
        },
    )
    def post(self, request):
        serializer = self.seralizer(data=request.data)

        if serializer.is_valid():
            response = self.service.validate_user(serializer)

            return Response(response, status=status.HTTP_200_OK)

        raise BadRequestException(serializer.errors)
