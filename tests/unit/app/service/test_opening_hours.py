import unittest

from src.app.request_parser.opening_hours_data_parser import OpeningHoursDataParser
from src.app.service.opening_hours import OpeningHoursService
from tests.fixtures.common import VALID_HUMAN_READABLE_OPENING_HOURS, VALID_PARSED_OPENING_HOURS, \
    VALID_OPENING_HOURS_OBJ, PARSED_OPENING_HOURS_DATA


class TestOpeningHoursService(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestOpeningHoursService, self).__init__(*args, **kwargs)
        self.opening_hours_service = OpeningHoursService()

    @unittest.mock.patch(
        'src.app.service.opening_hours.OpeningHoursService.parse_opening_hours',
        return_value=VALID_PARSED_OPENING_HOURS
    )
    @unittest.mock.patch(
        'src.app.utils.time_formatter.TimeFormatter.get_formatted_times_for_days',
        return_value=VALID_HUMAN_READABLE_OPENING_HOURS
    )
    def test_get_human_readable_opening_hours_returns_expected_data(self, formatted_time, parsed_hours):
        parsed_hours_data = self.opening_hours_service.get_human_readable_opening_hours(
            opening_hours=VALID_OPENING_HOURS_OBJ
        )
        self.assertEqual(parsed_hours_data, VALID_HUMAN_READABLE_OPENING_HOURS)

    def test_parsed_opening_hours_returns_expected_data(self):
        for opening_hours_data in PARSED_OPENING_HOURS_DATA:
            opening_hours = OpeningHoursDataParser(request_data=opening_hours_data[0]).get_model()
            parsed_open_hours = self.opening_hours_service.parse_opening_hours(opening_hours=opening_hours)
            self.assertEqual(parsed_open_hours, opening_hours_data[1])
