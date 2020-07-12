import pytest
from pydantic import ValidationError

from src.app.models.opening_hours import DayTimings
from tests.fixtures.opening_hours_model_data import INVALID_DAY_TIMINGS_DATA, VALID_DAY_TIMINGS_DATA


class TestDayTimingsModel:
    @pytest.mark.parametrize('day_timings,day,timings', VALID_DAY_TIMINGS_DATA)
    def test_valid_day_timings(self, day_timings: dict, day: str, timings):
        day_timing = DayTimings(**day_timings)
        assert day_timing.weekday == day
        assert day_timing.timings == timings

    @pytest.mark.parametrize('day_timings', INVALID_DAY_TIMINGS_DATA)
    def test_invalid_day_timings(self, day_timings: dict):
        try:
            _ = DayTimings(**day_timings)
        except ValidationError:
            pass
        else:
            pytest.fail('Invalid DayTimings data should have raised ValidationError')
