import pytest

from src.app.models.validators import strings_are_equal
from src.app.time_formatter import TimeFormatter
from tests.fixtures.time_formatter import DAY_TIMESTAMP_TO_HUMAN_READABLE, UNIX_TIMESTAMP_TO_HUMAN_READABLE, \
    FORMATTED_TIME_RANGES, FORMATTED_TIMES_FOR_DAY


class TestTimeFormatter:
    @pytest.mark.parametrize("timestamp,expected_time", DAY_TIMESTAMP_TO_HUMAN_READABLE)
    def test_human_readable_time_of_day_from_timestamp(self, timestamp, expected_time):
        assert TimeFormatter.get_human_readable_time_from_timestamp(timestamp) == expected_time

    @pytest.mark.parametrize("timestamp,expected_time", UNIX_TIMESTAMP_TO_HUMAN_READABLE)
    def test_human_readable_time_of_day_from_unix_timestamp(self, timestamp, expected_time):
        assert TimeFormatter.get_human_readable_time_from_timestamp(timestamp) == expected_time

    @pytest.mark.parametrize("opening_time,closing_time,time_range", FORMATTED_TIME_RANGES)
    def test_get_formatted_time_range(self, opening_time, closing_time, time_range):
        assert strings_are_equal(
            first=TimeFormatter.get_formatted_time_range(opening_time=opening_time, closing_time=closing_time),
            second=time_range,
            case_insensitive=False
        )

    @pytest.mark.parametrize("times_data,expected_result", FORMATTED_TIMES_FOR_DAY)
    def test_get_formatted_times_for_day(self, times_data, expected_result):
        assert TimeFormatter.get_formatted_times_for_days(times_data) == expected_result
