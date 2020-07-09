import copy
import os
import unittest

# pylint: disable=E0611
from src.lib.configuration.app_configuration import AppConfiguration
from .config_test_utils import YAML_CONFIG_DATA


# pylint: disable=invalid-name
class AppConfigurationTests(unittest.TestCase):
    def test_configuration_object_contains_all_data(self):
        configuration = AppConfiguration(**YAML_CONFIG_DATA)

        self.assertEqual(configuration.EndpointBaseUrl, YAML_CONFIG_DATA['EndpointBaseUrl'])
        self.assertEqual(configuration.Stage, YAML_CONFIG_DATA['Stage'])
        self.assertEqual(configuration.ServerPort, YAML_CONFIG_DATA['ServerPort'])
        self.assertTrue(configuration.Debug)

