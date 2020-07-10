from typing import Dict, Any

from src.app.time_formatter import TimeFormatter
from src.app.models.opening_hours import OpeningHours

OPEN_STATUS = 'open'
CLOSE_STATUS = 'close'


class OpeningHoursService:
    def __init__(self):
        pass

    def get_human_readable_opening_hours(self, opening_hours: OpeningHours) -> str:
        parsed_timings_data = self.parse_opening_hours(opening_hours)

        return TimeFormatter.get_formatted_times_for_days(parsed_timings_data)

    def parse_opening_hours(self, opening_hours: OpeningHours) -> Dict[str, Any]:
        opening_time = None
        opening_day = None
        next_day_closing = None

        day_opening_timings = dict()
        for each in opening_hours.sorted_weekdays:
            if each.timings is None:
                continue

            day_opening_timings[each.weekday] = []
            for timing_event in each.timings:
                if timing_event.status == OPEN_STATUS:
                    opening_time = TimeFormatter.get_human_readable_time_from_timestamp(timestamp=timing_event.value)
                    opening_day = each.weekday

                elif timing_event.status == CLOSE_STATUS:
                    closing_time = TimeFormatter.get_human_readable_time_from_timestamp(timestamp=timing_event.value)

                    if opening_time is not None:
                        day_opening_timings[opening_day].append(
                            TimeFormatter.get_formatted_time_range(opening_time, closing_time)
                        )

                    else:
                        next_day_closing = closing_time

        if next_day_closing:
            day_opening_timings[each.weekday].append(
                TimeFormatter.get_formatted_time_range(opening_time, next_day_closing))

        return day_opening_timings
