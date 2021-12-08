"""
File name: constants.py
Author: Fernando Rivera
Creation date: 2021-12-05
"""


class ExceptionConstants:
    """
    The exception constants.
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


class GenericConstants:
    """
    The generic constants.
    """

    DESCRIPTION = "description"
    """
    The description.
    """

    EMPTY_CHAR = ""
    """
    The empty char.
    """

    LINE_BREAK = "\n "
    """
    The line break character.
    """

    ID = "id"
    """
    The identifier.
    """

    NAME = "name"
    """
    The name.
    """

    PRODUCT = "product"
    """
    The product.
    """
