import unittest

import pytest

from src.app.time_formatter import TimeFormatter
from tests.fixtures.time_formatter import DAY_TIMESTAMP_TO_HUMAN_READABLE, UNIX_TIMESTAMP_TO_HUMAN_READABLE


# Cannot subclass this from unittest.TestCase because paramterization is not support
# https://docs.pytest.org/en/latest/unittest.html#pytest-features-in-unittest-testcase-subclasses
class TestTimeFormatter:
    @pytest.mark.parametrize("timestamp,expected_time", DAY_TIMESTAMP_TO_HUMAN_READABLE)
    def test_human_readable_time_of_day_from_timestamp(self, timestamp, expected_time):
        assert TimeFormatter.get_human_readable_time_from_timestamp(timestamp) == expected_time

    @pytest.mark.parametrize("timestamp,expected_time", UNIX_TIMESTAMP_TO_HUMAN_READABLE)
    def test_human_readable_time_of_day_from_unix_timestamp(self, timestamp, expected_time):
        assert TimeFormatter.get_human_readable_time_from_timestamp(timestamp) == expected_time


