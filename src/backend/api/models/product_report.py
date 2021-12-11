"""
File name: product.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from utils.exceptions.api_exceptions import InternalServerErrorException


class ProductReport:
    """
    Thge product report object.
    """

    def __init__(self, id, name, description, total_quantity, total_price):
        """
        Initializes a new instance of ProductReport object.

        :param uuid4 id: The product identifier.
        :param string name: The product name.
        :param string description: The product description.
        :param int total_quantity: The product sold total quantity.
        :param int total_price: The product sold total price.
        """
        self.id = id
        self.name = name
        self.description = description
        self.total_quantity = total_quantity
        self.total_price = total_price
