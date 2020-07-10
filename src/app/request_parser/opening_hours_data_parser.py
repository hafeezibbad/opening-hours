from pydantic import ValidationError

from src.app.models.opening_hours import TimeEntry, OpeningHours, DayTimings
from src.app.request_parser.data_parser import RequestDataParser


class OpeningHoursDataParser(RequestDataParser):
    def __init__(self, request_data: dict) -> None:
        super(OpeningHoursDataParser, self).__init__(request_data)
        self.__validate(data=request_data)

    def get_model(self):
        return self.model

    def is_valid(self):
        return not self.api_error

    def __validate(self, data: dict):
        try:
            opening_hours_data = dict()

            for day, opening_times in data.items():
                day_opening_times = []
                for opening_time in opening_times:
                    # Make timing event input case-insensitive
                    opening_time = {k.lower(): v for k, v in opening_time.items()}
                    day_opening_times.append(
                        TimeEntry.load(data=opening_time, overridden_field_names={'type': 'status'})
                    )

                day_timings = DayTimings.load({'weekday': day, 'timings': day_opening_times})

                opening_hours_data[day.lower()] = day_timings

            self.model = OpeningHours(**opening_hours_data)

        except ValidationError as ex:
            self.api_error = self._handle_pydantic_validation_error(ex, overridden_field_names={'status': 'type'})
