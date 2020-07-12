from typing import Dict, Any, Optional

from src.app.models.constants import STATUS_OPEN, STATUS_CLOSE
from src.app.models.validators import strings_are_equal
from src.app.time_formatter import TimeFormatter
from src.app.models.opening_hours import OpeningHours, DayTimings


class OpeningHoursService:
    def get_human_readable_opening_hours(self, opening_hours: OpeningHours) -> str:
        parsed_timings_data = self.parse_opening_hours(opening_hours)

        return TimeFormatter.get_formatted_times_for_days(parsed_timings_data)

    def parse_opening_hours(self, opening_hours: OpeningHours) -> Dict[str, Any]:
        opening_time = None
        opening_day = None
        next_day_closing = None
        last_event_is_open = None

        day_opening_timings = dict()
        timing_data: Optional[DayTimings] = None
        for timing_data in opening_hours.sorted_weekdays:
            if timing_data.timings is None:
                continue

            day_opening_timings[timing_data.weekday] = []
            for timing_event in timing_data.timings:
                if strings_are_equal(timing_event.status, STATUS_OPEN):
                    opening_time = TimeFormatter.get_human_readable_time_from_timestamp(timestamp=timing_event.value)
                    opening_day = timing_data.weekday
                    last_event_is_open = True

                elif strings_are_equal(timing_event.status, STATUS_CLOSE):
                    last_event_is_open = False
                    closing_time = TimeFormatter.get_human_readable_time_from_timestamp(timestamp=timing_event.value)
                    if opening_time is not None:
                        day_opening_timings[opening_day].append(
                            TimeFormatter.get_formatted_time_range(opening_time, closing_time)
                        )

                    else:
                        next_day_closing = closing_time

        if timing_data is not None:
            if last_event_is_open and strings_are_equal(timing_data.weekday, 'sunday'):
                day_opening_timings[timing_data.weekday].append(
                    TimeFormatter.get_formatted_time_range(opening_time, '')
                )

            # Edge case # 5: First event of week is a closing event
            elif next_day_closing and day_opening_timings.get(timing_data.weekday) is not None:
                day_opening_timings[timing_data.weekday].append(
                    TimeFormatter.get_formatted_time_range(opening_time, next_day_closing)
                )

        return day_opening_timings
