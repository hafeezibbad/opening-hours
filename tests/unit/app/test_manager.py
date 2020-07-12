import unittest
from json.decoder import JSONDecodeError

import pytest

from src.app.models.opening_hours import OpeningHours
from src.app.models.status import Status
from src.app.errors import AppSimpleError, AppErrorType
from src.app.manager import AppManager
from src.app.request_parser.opening_hours_data_parser import OpeningHoursDataParser
from tests.fixtures.common import VALID_JSON_STRING, VALID_HUMAN_READABLE_OPENING_HOURS, VALID_REQUEST_DATA
from tests.fixtures.opening_hours_model_data import VALID_OPENING_HOURS
from tests.fixtures.service_status import SERVICE_UP_STATUS, SERVICE_DOWN_STATUS


class TestOpeningHoursAppManager(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestOpeningHoursAppManager, self).__init__(*args, **kwargs)
        self.app_manager = AppManager()

    @unittest.mock.patch('src.app.service.health_check.HealthCheckService.check_all', return_value=True)
    def test_status_returns_down_if_service_is_down(self, health_check_mock):
        status: Status = self.app_manager.status()
        self.assertEqual(status, SERVICE_UP_STATUS)

    @unittest.mock.patch('src.app.service.health_check.HealthCheckService.check_all', return_value=False)
    def test_status_returns_ok_if_service_is_up(self, health_check_mock):
        status: Status = self.app_manager.status()
        self.assertEqual(status, SERVICE_DOWN_STATUS)

    def test_parse_request_data_raise_error_if_json_is_none_or_empty(self):
        for data in ['', None]:
            try:
                _ = self.app_manager.parse_request_data_as_json(request_data=data)

            except AppSimpleError as ex:
                self.assertEqual(AppErrorType.REQUEST_BODY_EMPTY[0], ex.code)
                self.assertEqual(AppErrorType.REQUEST_BODY_EMPTY[1], ex.http_status)
                self.assertEqual('No JSON data provided in request body', ex.message)

            else:
                pytest.fail('AppSimpleError muse be raised when request_data is {}'.format(data))

    @unittest.mock.patch('json.loads')
    def test_parse_request_data_raise_error_if_json_is_invalid(self, json_mock):
        json_mock.side_effect = JSONDecodeError(msg='', doc='', pos=0)
        try:
            _ = self.app_manager.parse_request_data_as_json(request_data=VALID_JSON_STRING)

        except AppSimpleError as ex:
            self.assertEqual(AppErrorType.REQUEST_BODY_INVALID_JSON[0], ex.code)
            self.assertEqual(AppErrorType.REQUEST_BODY_INVALID_JSON[1], ex.http_status)
            self.assertEqual('Invalid JSON format provided in request body', ex.message)

        else:
            pytest.fail('AppSimpleError muse be raised')

    @unittest.mock.patch(
        'src.app.request_parser.opening_hours_data_parser.OpeningHoursDataParser.get_model',
        return_value=OpeningHours.load(VALID_OPENING_HOURS[0][0])
    )
    @unittest.mock.patch(
        'src.app.request_parser.opening_hours_data_parser.OpeningHoursDataParser.is_valid',
        return_value=True
    )
    @unittest.mock.patch(
        'src.app.request_parser.opening_hours_data_parser.OpeningHoursDataParser.__init__',
        return_value=None
    )
    def test_parse_request_data_returns_expected_model(self, parser, is_valid, api_error):
        opening_hours = self.app_manager.parse_request_data(
            parser=OpeningHoursDataParser,
            request_data=VALID_OPENING_HOURS[0]
        )
        self.assertEqual(opening_hours, OpeningHours.load(VALID_OPENING_HOURS[0][0]))

    @unittest.mock.patch(
        'src.app.manager.AppManager.parse_request_data',
        return_value=OpeningHours.load(VALID_OPENING_HOURS[0][0])
    )
    @unittest.mock.patch(
        'src.app.service.opening_hours.OpeningHoursService.get_human_readable_opening_hours',
        return_value=VALID_HUMAN_READABLE_OPENING_HOURS
    )
    def test_get_human_readable_opening_hours_return_expected_data(self, human_readable_hours, parsed_data):
        opening_hours = self.app_manager.get_human_readable_opening_hours(request_data=VALID_REQUEST_DATA)
        self.assertEqual(opening_hours, VALID_HUMAN_READABLE_OPENING_HOURS)
