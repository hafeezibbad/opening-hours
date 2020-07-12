import pytest
from pydantic import ValidationError

from src.app.models.opening_hours import OpeningHours
from tests.fixtures.opening_hours_model_data import VALID_OPENING_HOURS, INVALID_OPENING_HOURS


class TestOpeningHoursModel:
    @pytest.mark.parametrize('opening_hours,day,timings', VALID_OPENING_HOURS)
    def test_valid_opening_hours(self, opening_hours, day, timings):
        opening_hours = OpeningHours(**opening_hours)
        assert getattr(opening_hours, day) is not None
        assert getattr(opening_hours, day) == timings

    @pytest.mark.parametrize('opening_hours', INVALID_OPENING_HOURS)
    def test_invalid_opening_hours(self, opening_hours):
        try:
            _ = OpeningHours(**opening_hours)
        except ValidationError:
            pass
        else:
            pytest.fail('Invalid OpeningHours data should have raised ValidationError')
