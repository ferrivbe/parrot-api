"""
File name: test_apps.py
Author: Fernando Rivera
Creation date: 2021-12-07
"""
from django.apps import apps

from api.apps import ApiConfig


class ApiConfigTestCase:
    """
    The api apps testing class.
    """

    def test_apps(self):
        """
        Tests the api apps.py file
        """
        assert ApiConfig.name == "api"
        assert apps.get_app_config("api").name == "api"
