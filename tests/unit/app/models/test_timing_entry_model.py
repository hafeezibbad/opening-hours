import pytest
from pydantic import ValidationError

from src.app.models.opening_hours import TimeEntry
from tests.fixtures.opening_hours_model_data import VALID_TIME_ENTRY_DATA, INVALID_TIME_ENTRY_DATA


class TestDayTimingsModel:
    @pytest.mark.parametrize('time_entry,status,value', VALID_TIME_ENTRY_DATA)
    def test_valid_time_entries(self, time_entry: dict, status: str, value):
        time_entry = TimeEntry(**time_entry)
        assert time_entry.status == status
        assert time_entry.value == value

    @pytest.mark.parametrize('time_entry', INVALID_TIME_ENTRY_DATA)
    def test_invalid_time_entries(self, time_entry: dict):
        try:
            _ = TimeEntry(**time_entry)
        except ValidationError:
            pass
        else:
            pytest.fail('Invalid TimeEntry data should have raised ValidationError')
