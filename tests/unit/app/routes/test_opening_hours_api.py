from unittest.mock import patch

from flask import Response

from src.app.errors import DataParsingError, AppError, AppErrorType
from tests.fixtures.opening_hours_data import VALID_OPENING_HOURS
from tests.unit.app.routes.common import BaseTests
from tests.unit.app.routes.flask_api_response import FlaskApiResponse
from tests.unit.app.routes.request_utils import post_opening_hours_request
from tests.unit.lib.configuration.config_test_utils import MOCK_CONFIGURATION_OBJ


@patch('src.flask_app.load_configuration_from_yaml_file', return_value=MOCK_CONFIGURATION_OBJ)
class TestOpeningHoursApi(BaseTests):

    @patch('src.app.manager.AppManager.get_human_readable_opening_hours')
    def test_opening_hours_api_returns_200_ok(self, get_human_readable_hours, app_config):
        for opening_hours_data in VALID_OPENING_HOURS:
            get_human_readable_hours.return_value = opening_hours_data[1]

            response: FlaskApiResponse = post_opening_hours_request(request_data=opening_hours_data[0])

            response.status_code_is_200_ok()
            response.contains_request_id()

            response.text_data_is(expected_response_text=opening_hours_data[1])

    @patch('src.app.routes.opening_hours.handle_and_log_service_exception', return_value=Response())
    @patch('src.app.manager.AppManager.get_human_readable_opening_hours')
    def test_data_parsing_error_is_handled_and_logged(
            self,
            get_human_readable_hours,
            handle_and_log_service_exception,
            app_config
    ):
        exception = DataParsingError(title='Data parsing error', detail='Data parsing error')
        get_human_readable_hours.side_effect = exception

        response: FlaskApiResponse = post_opening_hours_request(request_data=VALID_OPENING_HOURS[0][0])

        handle_and_log_service_exception.assert_called_with(
            exception,
            service_name="Opening hours app",
            message="Opening hours parsing failed"
        )

    @patch('src.app.routes.opening_hours.handle_and_log_service_exception', return_value=Response())
    @patch('src.app.manager.AppManager.get_human_readable_opening_hours')
    def test_api_error_is_handled_and_logged(
            self,
            get_human_readable_hours,
            handle_and_log_service_exception,
            app_config
    ):
        exception = AppError(code=AppErrorType.INTERNAL_SERVER_ERROR)
        get_human_readable_hours.side_effect = exception

        response: FlaskApiResponse = post_opening_hours_request(request_data=VALID_OPENING_HOURS[0][0])

        handle_and_log_service_exception.assert_called_with(
            exception,
            service_name="Opening hours app",
            message='Opening hours parsing failed'
        )

    @patch('src.app.routes.opening_hours.handle_and_log_unknown_exception', return_value=Response())
    @patch('src.app.manager.AppManager.get_human_readable_opening_hours')
    def test_unknown_error_is_handled_and_logged(
            self,
            get_human_readable_hours,
            handle_and_log_unknown_exception,
            app_config
    ):
        exception = ValueError()
        get_human_readable_hours.side_effect = exception

        response: FlaskApiResponse = post_opening_hours_request(request_data=VALID_OPENING_HOURS[0][0])

        handle_and_log_unknown_exception.assert_called_with(
            exception,
            message='Unknown exception'
        )
