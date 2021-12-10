"""
File name: constants.py
Author: Fernando Rivera
Creation date: 2021-12-05
"""


class ExceptionConstants:
    """
    The exception constants.
    """

    EMAIL_ALREADY_EXISTS = "Email already exists."
    """
    The exception when email already exists.
    """

    EMAIL_MUST_BE_SET = "The email must be set."
    """
    The exception when email is not set.
    """

    EXTERNAL_CLIENT_NAME_MISSING = "The external client name is missing."
    """
    The exception when the external client name is missing.
    """

    INVALID_CREDENTIALS = "Invalid password or credentials."
    """
    The exception when the credentials are invalid.
    """

    NAME_ALREADY_IN_USE = "The name '%(name)s' is already in use."
    """
    The exception when a user name already exists.
    """

    ORDER_IS_CLOSED = "The order with id '%(id)s' is closed, no changes allowed"
    """
    The exception when order is closed.
    """

    ORDER_NOT_FOUND = "The order with identifier '%(id)s' does not exist."
    """
    The exception when an order is not found.
    """

    PRODUCT_BY_ID_NOT_FOUND = "The product with id '%(id)s' does not exist."
    """
    The exception when a product by identifier does not exists.
    """

    PRODUCT_BY_NAME_EXISTS = "The product with name '%(name)s already exists."
    """
    The exception when a product by name already exists.
    """

    PRODUCT_NAME_IS_REQUIRED = "The product requires a valid name"
    """
    The exception when the product name is not provided.
    """

    PRODUCT_NOT_AVAILABLE = (
        "The product with id '%(id)s' does not exist or is no longer available."
    )
    """
    Th exception when product is deleted or does not exist.
    """

    PARAMETER_INVALID_BY_REGEX = (
        "This parameter does not comply with allowed characters."
    )
    """
    The exception when a parameter is invalid due to regex validation.
    """

    PASSWORD_MUST_BE_SET = "The password must be set"
    """
    The exception when password is not set.
    """

    QUANTITY_FOR_PRODUCT_EXISTS = (
        "A product quantity for product with id '%(id)s' already exists."
    )
    """
    The exception when a product quantity for product id already exists.
    """

    QUANTITY_FOR_PRODUCT_NOT_FOUND = (
        "The product quantity for product with id '%(id)s' does not exist."
    )
    """
    The exception when a product quantity by identifier does not exist.
    """

    SUPER_USER_ROLE_INVALID = "Superuser must have role of Global Admin"
    """
    The exception when a user is not an admin.
    """

    USER_BY_EMAIL_NOT_FOUND = "User with email '%(email)s' not found."
    """
    The exception when user by email not found.
    """

    USER_BY_ID_NOT_FOUND = "User with id '%(id)s' not found."
    """
    The exception when user by id not found.
    """

    USER_CREATION_ROLE_NOT_VALID = "A user with role '%(creator_role)s', cannot crate a new user with role '%(user_role)s'."
    """
    The exception when user creation with role not valid.
    """

    USER_ROLE_NOT_VALID = "A user with role '%(role)s' cannot perform this action."
    """
    The exception when user role not valid.
    """

    VALID_PRICE_MUST_BE_SET = "A valid price, greater than zero, must be set."
    """
    The exception when price is None or lower than zero.
    """

    VALID_QUANTITY_MUST_BE_SET = "A valid quantity, greater than zero, must be set."
    """
    The exception when quantity is None or lower than zero.
    """


class GenericConstants:
    """
    The generic constants.
    """

    ACCESS_TOKEN = "access_token"
    """
    The access token.
    """

    CREATOR_ROLE = "creator_role"
    """
    The creator role.
    """

    DATE = "date"
    """
    The date.
    """

    DELETED_AT = "deleted_at"
    """
    The deletion date.
    """

    DESCRIPTION = "description"
    """
    The description.
    """

    EMAIL = "email"
    """
    The email.
    """

    EMPTY_CHAR = ""
    """
    The empty char.
    """

    EXPIRES_IN = "expires_in"
    """
    The expiration time.
    """

    EXTERNAL_CLIENT = "external_client"
    """
    The external client.
    """

    FIRST_NAME = "first_name"
    """
    The first name.
    """

    ID = "id"
    """
    The identifier.
    """

    IS_ACTIVE = "is_active"
    """
    The is active flag.
    """

    LAST_NAME = "last_name"
    """
    The last name.
    """

    LINE_BREAK = "\n "
    """
    The line break character.
    """

    NAME = "name"
    """
    The name.
    """

    NEGATIVE_INDEX = -1
    """
    The negative index.
    """

    ORDER = "order"
    """
    The order.
    """

    PARAMETER = "parameter"
    """
    The parameter.
    """

    PASSWORD = "password"
    """
    The password.
    """

    PRICE = "price"
    """
    The price.
    """

    PRODUCT = "product"
    """
    The product.
    """

    PRODUCT_QUANTITIES = "product_quantities"
    """
    The product quantities.
    """

    PRODUCT_QUANTITY = "product_quantity"
    """
    The product quantity.
    """

    QUANTITY = "quantity"
    """
    The quantity.
    """

    REFRESH_TOKEN = "refresh_token"
    """
    The refresh token.
    """

    ROLE = "role"
    """
    The role.
    """

    SPACE = " "
    """
    The space.
    """

    TOTAL_PRICE = "total_price"
    """
    The total price.
    """

    USER = "user"
    """
    The user.
    """

    USERS = "users"
    """
    The users.
    """

    USER_ROLE = "user_role"
    """
    The user role.
    """


class ValidationConstants:
    """
    The validation constants.
    """

    LATIN_SPECIAL_CHAR_REGEX = "^[A-Z a-z Ñ ñ . ' _]+$"
    """
    The latin with special characters REGEX.
    """
