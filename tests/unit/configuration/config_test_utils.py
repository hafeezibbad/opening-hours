import os
from collections import defaultdict
from unittest.mock import patch

from munch import DefaultMunch

from src.lib.configuration.utils import load_configuration_from_yaml_file


MOCK_YAML_CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'test_files/mock_configuration.yml')
MOCK_JSON_CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'test_files/config.json')
TEST_FILES_DIRECTORY_PATH = os.path.join(os.path.dirname(__file__), 'test_files')


YAML_CONFIG_DATA = {
    "Stage": "dev",
    "ServerPort": 3500,
    "EndpointBaseUrl": "http://localhost:3500",
    "Debug": True
}

MOCK_OS_ENVIRON = DefaultMunch('', {'APP_CONFIG_FILE': ''})


MOCK_CONFIGURATION_OBJ = load_configuration_from_yaml_file(config_file_path=MOCK_YAML_CONFIG_FILE_PATH)


def exception_must_contain_configuration_error(ex, configuration_error):
    assert ex.code == configuration_error[0]
    assert ex.event_name == configuration_error[2]
