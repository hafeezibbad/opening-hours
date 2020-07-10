import os
import unittest

# pylint: disable=no-name-in-module
from tests.fixtures.common import REQUEST_ID_STARTS_WITH, REQUEST_ID_LENGTH
from tests.unit.configuration.config_test_utils import MOCK_CONFIGURATION_OBJ, MOCK_OS_ENVIRON


with unittest.mock.patch.dict(os.environ, MOCK_OS_ENVIRON):
    with unittest.mock.patch(
            'src.lib.configuration.utils.load_configuration_from_yaml_file', return_value=MOCK_CONFIGURATION_OBJ
    ):
        from src.flask_app import app


def client():
    app.config['TESTING'] = True
    test_client = app.test_client()

    return test_client


# pylint: disable=redefined-outer-name
class BaseTests(unittest.TestCase):

    def client(self):
        app.config['TESTING'] = True
        client = app.test_client()

        return client


def method_will_raise_exception(mock_method, exception_type=OSError):
    mock_method.side_effect = exception_type('Test error')


def exception_type_should_be_valid(msg_types):
    assert 'exception' in msg_types


def request_id_must_be_valid(request_id):
    assert request_id.startswith(REQUEST_ID_STARTS_WITH)
    assert len(request_id) == REQUEST_ID_LENGTH


def exception_log_must_contain_valid_request_id(log_mock):
    if log_mock.fatal.called:
        log_args = log_mock.fatal.call_args[1]
    else:
        log_args = log_mock.error.call_args[1]

    request_id_key = 'request_id'
    assert request_id_key in log_args
    request_id_must_be_valid(log_args.get(request_id_key))


def exception_log_must_not_contain_request_id(log_mock, request_id):
    if log_mock.fatal.called:
        log_args = log_mock.fatal.call_args[1]
    else:
        log_args = log_mock.error.call_args[1]

    request_id_key = 'request_id'
    assert request_id_key in log_args
    assert log_args.get(request_id_key) != request_id
