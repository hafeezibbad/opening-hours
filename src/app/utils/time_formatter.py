from datetime import datetime
from typing import Dict, Optional

from pydantic import conint  # pylint: disable=no-name-in-module


class TimeFormatter:
    @staticmethod
    def get_human_readable_time_from_timestamp(timestamp: conint(ge=0, le=86399)) -> str:  # type: ignore
        _time_resolution = "%-I"
        _dt = datetime.utcfromtimestamp(timestamp)
        if _dt.minute > 0:
            _time_resolution = "%-I:%M"
        if _dt.second > 0:
            _time_resolution = "%-I:%M:%S"

        return _dt.strftime('{resolution} %p'.format(resolution=_time_resolution))

    @staticmethod
    def get_formatted_time_range(opening_time: Optional[str], closing_time: Optional[str]) -> str:
        return "{opening_time} - {closing_time}".format(opening_time=opening_time, closing_time=closing_time)

    @staticmethod
    def get_formatted_times_for_days(timing_data: Dict[str, str]) -> str:
        times = []
        for weekday, timings in timing_data.items():
            if timings:
                times.append("{day}: {timings}".format(
                    day=weekday.title(),
                    timings=', '.join([timing.upper() for timing in timings]).strip()
                ))
            else:
                times.append("{day}: Closed".format(day=weekday.title()))

        return "\n".join(times)
