import unittest.mock

from flask import Response

from tests.unit.configuration.config_test_utils import MOCK_CONFIGURATION_OBJ
from .common import BaseTests, method_will_raise_exception, exception_log_must_contain_valid_request_id, \
    exception_log_must_not_contain_request_id
from .request_utils import get_status_request


@unittest.mock.patch(
    'src.flask_app.load_configuration_from_yaml_file',
    return_value=MOCK_CONFIGURATION_OBJ
)
class FlaskAppGetStatusTests(BaseTests):
    @unittest.mock.patch('src.service.health_check.HealthCheckService.check_all')
    def test_get_status_ok(self, check_all, app_config_mock):
        check_all.return_value = True
        response = get_status_request()

        response.status_code_is_200_ok()
        response.health_check_status_is_up()
        response.contains_request_id()

        self.assertEqual(check_all.call_count, 1)

    # @unittest.mock.patch('src.service.health.HealthCheckService.check_all')
    # def test_get_status_down(self, check_all, app_config_mock):
    #     check_all.return_value = False
    #     response = get_status_request()
    #
    #     response.status_code_is_503_service_unavailable()
    #     response.body_contains_field('status', expected_value='down')
    #     self.assertEqual(check_all.call_count, 1)
    #
    # @unittest.mock.patch('src.service.health.HealthCheckService.check_all')
    # def test_get_status_exception_returns_500(self, check_all, app_config_mock):
    #     method_will_raise_exception(check_all)
    #     check_all.return_value = True
    #
    #     response = get_status_request()
    #
    #     response.status_code_is_500_internal_server_error()
    #
    # @unittest.mock.patch('src.service.health.HealthCheckService.check_all')
    # @unittest.mock.patch(
    #     'src.routes.status_api.handle_and_log_service_exception',
    #     return_value=Response(status=500)
    # )
    # def test_get_status_exception_log_called(self, log_unknown_exception, check_all, app_config_mock):
    #     method_will_raise_exception(check_all)
    #
    #     response = get_status_request()
    #     response.status_code_is_500_internal_server_error()
    #
    #     log_unknown_exception.assert_called()
    #
    # @unittest.mock.patch('src.service.health.HealthCheckService.check_all')
    # @unittest.mock.patch('src.lib.errors.exceptions.LOGGING')
    # def test_get_status_exception_log_has_tx_id(self, logging, check_all, app_config_mock):
    #     method_will_raise_exception(check_all)
    #
    #     response = get_status_request()
    #     response.status_code_is_500_internal_server_error()
    #     response.contains_transaction_id()
    #     exception_log_must_contain_valid_request_id(logging)
    #
    # @unittest.mock.patch('src.service.health.HealthCheckService.check_all')
    # @unittest.mock.patch('src.lib.errors.exceptions.LOGGING')
    # def test_get_pairing_key_ex_invalid_tx_id_gets_renewed(self, logging, check_all, app_config_mock):
    #     method_will_raise_exception(check_all)
    #     invalid_request_id = 'invalid-request-id'
    #
    #     response = get_status_request(request_id=invalid_request_id)
    #     response.status_code_is_500_internal_server_error()
    #
    #     exception_log_must_not_contain_request_id(logging, invalid_request_id)
    #     exception_log_must_contain_valid_request_id(logging)
    #
    # @unittest.mock.patch('src.service.health.HealthCheckService.check_all')
    # @unittest.mock.patch('fs.sensesdk.pairing.healthcheck.helper.HealthCheckHelper.status')
    # @unittest.mock.patch('fs.sensesdk.pairing.flask_app.LOGGING.info')
    # def test_status_check_logs_health_check_status(self, logging, check_status, check_all, app_config_mock):
    #     check_all.return_value = True
    #     check_status.return_value = dict()
    #
    #     response = get_status_request()
    #
    #     check_all.assert_called()
    #     check_status.assert_called()
    #     logging.assert_called()
    #     logging.assert_has_calls([unittest.mock.call('HEALTH_CHECK_STATUS', health_check_data=dict())])
