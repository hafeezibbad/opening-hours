import operator
import re
from typing import List, Optional, Dict, Any, Union

from pydantic import conint  # pylint: disable=no-name-in-module

from src.app.errors import DataParsingError
from src.app.utils.time_formatter import TimeFormatter

from .common import Model
from .constants import OPENING_STATUS_REGEX, STATUS_OPEN, STATUS_CLOSE, STATUS_CHOICES
from .validators import WeekdayStr, strings_are_equal, strings_are_not_equal


class OpeningStatusStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, status_type: str):
        if not isinstance(status_type, str):
            raise ValueError('Invalid `type`: str expected, `{}` provided'.format(type(status_type)))

        if not status_type.strip():
            raise ValueError('Empty string provided as status')

        if re.match(pattern=OPENING_STATUS_REGEX, string=status_type.strip(), flags=re.IGNORECASE) is None:
            raise ValueError('Invalid `type`. Choices are `{}`'.format(', '.join(STATUS_CHOICES)))

        return status_type


class TimeEntry(Model):
    status: OpeningStatusStr
    value: conint(ge=0, le=86399)  # type: ignore

    def dict(self, *args, **kwargs) -> Dict[str, Union[int, str]]:
        return {
            "type": self.status,
            "value": self.value
        }


class ValidDayTimings(list):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, timings):
        if not isinstance(timings, list):
            raise ValueError('Invalid input: list expected, `{}` provided'.format(type(timings)))

        if not all([isinstance(each, TimeEntry) for each in timings]):
            raise ValueError('Invalid items in timings')

        timings = sorted(timings, key=operator.attrgetter("value"))

        if ValidDayTimings.check_duplicate_consecutive_events_exist(timings) is True:
            raise DataParsingError(
                title="Invalid event sequence",
                detail="Overlapping intervals or consecutive events of same `type`",
                source=[timing.dict() for timing in timings]
            )

        if ValidDayTimings.check_different_events_at_same_time_exist(timings) is True:
            raise DataParsingError(
                title="Invalid event sequence",
                detail='Different events specified with same `value`',
                source=[timing.dict() for timing in timings]
            )

        return timings

    @classmethod
    def check_duplicate_consecutive_events_exist(cls, timings: List[TimeEntry]) -> bool:
        previous_timing_event: Optional[str] = None
        for each in timings:
            if each.status == previous_timing_event:
                return True
            previous_timing_event = each.status

        return False

    @classmethod
    def check_different_events_at_same_time_exist(cls, timings: List[TimeEntry]) -> bool:
        event_times = dict()
        for each in timings:
            if each.value not in event_times:
                event_times[each.value] = each.status

            elif strings_are_not_equal(event_times[each.value], each.status):
                return True

        return False


class DayTimings(Model):
    weekday: WeekdayStr
    timings: Optional[ValidDayTimings] = None


class OpeningHours(Model):
    monday: DayTimings = DayTimings.load({"weekday": "monday"})
    tuesday: DayTimings = DayTimings.load({"weekday": "tuesday"})
    wednesday: DayTimings = DayTimings.load({"weekday": "wednesday"})
    thursday: DayTimings = DayTimings.load({"weekday": "thursday"})
    friday: DayTimings = DayTimings.load({"weekday": "friday"})
    saturday: DayTimings = DayTimings.load({"weekday": "saturday"})
    sunday: DayTimings = DayTimings.load({"weekday": "sunday"})

    @property
    def sorted_weekdays(self):
        return [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday, self.sunday]

    def raise_parsing_error(self, title: str, error_data: dict, source_pointer: Any):
        error_data = error_data or {}

        error_detail: str = '`{last_day}: {last_time}` has no {timing_event} time{suffix}'.format(
            last_day=error_data.get('last_day', '').title(),
            # FIXME: Here we can actually give the user provided value
            last_time=TimeFormatter.get_human_readable_time_from_timestamp(error_data.get('last_time', 0)),
            timing_event=error_data.get('timing_event', ''),
            suffix=error_data.get('error_msg_suffix', '')
        )

        raise DataParsingError(
            title=title,
            detail=error_detail,
            source=dict(pointer=source_pointer)
        )

    def validate_all_open_time_have_closing_times(self):
        last_event_status: str = ''
        last_open_time: int = 0
        last_open_day: str = ''
        last_day_with_timings: str = ''
        days_with_events: int = 0
        for i, day in enumerate(self.sorted_weekdays):
            if day.timings is None:
                continue

            # To address corner case # 1
            if last_open_day \
                    and strings_are_not_equal(last_open_day, day.weekday) \
                    and strings_are_not_equal(last_open_day, self.sorted_weekdays[i-1].weekday):
                self.raise_parsing_error(
                    title='Missing closing time',
                    source_pointer=last_open_day,
                    error_data=dict(
                        last_day=last_day_with_timings,
                        last_time=last_open_time,
                        timing_event='closing',
                        error_msg_suffix=' on following day'
                    )
                )

            for each in day.timings:
                last_day_with_timings = day.weekday
                days_with_events += 1
                if strings_are_equal(last_event_status, each.status):
                    if strings_are_equal(each.status, STATUS_OPEN):
                        error_data = dict(timing_event='closing', last_day=last_open_day, last_time=last_open_time)
                    else:
                        error_data = dict(timing_event='opening', last_day=day.weekday, last_time=each.value)

                    self.raise_parsing_error(
                        title='Missing {} times'.format(error_data.get('timing_event', '')),
                        source_pointer=error_data.get('last_day'),
                        error_data=error_data
                    )

                elif strings_are_equal(each.status, STATUS_OPEN):
                    last_event_status = STATUS_OPEN
                    last_open_time = each.value
                    last_open_day = day.weekday

                elif strings_are_equal(each.status, STATUS_CLOSE):
                    last_event_status = STATUS_CLOSE
                    last_open_day = ''

        if last_day_with_timings \
                and strings_are_not_equal(last_day_with_timings, 'sunday') \
                and strings_are_equal(last_event_status, STATUS_OPEN):
            self.raise_parsing_error(
                title='Missing closing time',
                source_pointer=last_open_day,
                error_data=dict(
                    last_day=last_open_day,
                    last_time=last_open_time,
                    timing_event='closing'
                )
            )

    def __init__(self, **kwargs) -> None:
        super(OpeningHours, self).__init__(**kwargs)
        self.validate_all_open_time_have_closing_times()
