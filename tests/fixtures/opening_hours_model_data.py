from typing import Optional

from src.app.models.opening_hours import TimeEntry, DayTimings

VALID_TIME_ENTRY_DATA = [
    ({"status": "open", "value": 0}, "open", 0),
    ({"status": "open", "value": 86399}, "open", 86399),
    ({"status": "close", "value": 0}, "close", 0),
    ({"status": "close", "value": 86399}, "close", 86399),
    ({"status": "Open", "value": 0}, "Open", 0),
    ({"status": "OPEN", "value": 86399}, "OPEN", 86399),
    ({"status": "Close", "value": 0}, "Close", 0),
    ({"status": "CLOSE", "value": 86399}, "CLOSE", 86399),
    ({"status": "open", "value": "0"}, "open", 0),
    ({"status": "close", "value": "86399"}, "close", 86399)
]

INVALID_TIME_ENTRY_DATA = [
    {"status": "invalid", "value": 0},
    {"status": "open", "value": -1},
    {"status": "open", "value": 86400},
    {"status": None, "value": 1},
    {"status": "open", "value": None},
    {"status": 123, "value": 1},
]

TEST_TIMINGS = [
    TimeEntry.load({"status": "open", "value": 3600}),
    TimeEntry.load({"status": "close", "value": 6400})
]

VALID_DAY_TIMINGS_DATA = [
    ({"weekday": "monday", "timings": []}, "monday", []),
    ({"weekday": "TUESDAY", "timings": []}, "TUESDAY", []),
    ({"weekday": "Wednesday", "timings": []}, "Wednesday", []),
    ({"weekday": "thursday", "timings": []}, "thursday", []),
    ({"weekday": "friday", "timings": []}, "friday", []),
    ({"weekday": "SaturDay", "timings": []}, "SaturDay", []),
    ({"weekday": "Sunday", "timings": []}, "Sunday", []),
    ({"weekday": "Sunday", "timings": []}, "Sunday", []),
    ({"weekday": "monday", "timings": None}, "monday", None),
    ({"weekday": "monday", "timings": None}, "monday", None),
    ({"weekday": "monday", "timings": TEST_TIMINGS}, "monday", TEST_TIMINGS),
]

INVALID_DAY_TIMINGS_DATA = [
    {"weekday": "invalid_day", "timings": []},
    {"weekday": 123, "timings": []},
    {"weekday": None, "timings": []},
    {"weekday": "monday", "timings": "123"},
    {"weekday": "monday", "timings": "string_timing"},
    {"weekday": "monday", "timings": 123},
]


# pylint: disable=dangerous-default-value
def get_day_timings(day: str, day_timings: Optional[list] = TEST_TIMINGS) -> DayTimings:
    return DayTimings.load({"weekday": day, "timings": day_timings})


VALID_OPENING_HOURS = [
    ({"monday": get_day_timings(day="monday")}, "monday", get_day_timings("monday")),
    ({"tuesday": get_day_timings(day="tuesday")}, "tuesday", get_day_timings("tuesday")),
    ({"wednesday": get_day_timings(day="wednesday")}, "wednesday", get_day_timings("wednesday")),
    ({"thursday": get_day_timings(day="thursday")}, "thursday", get_day_timings("thursday")),
    ({"friday": get_day_timings(day="friday")}, "friday", get_day_timings("friday")),
    ({"saturday": get_day_timings(day="saturday")}, "saturday", get_day_timings("saturday")),
    ({"sunday": get_day_timings(day="sunday")}, "sunday", get_day_timings("sunday"))
]

INVALID_OPENING_HOURS = [
    {"monday": "random_value"},
    {"monday": None},
    {"monday": 123},
    {"monday": []},
    {"monday": {}},
]
