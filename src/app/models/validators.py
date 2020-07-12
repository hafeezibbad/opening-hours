import re

from .constants import WEEKDAY_REGEX


class StrictNonEmptyStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise ValueError('Invalid `type`: str expected, `{}` provided'.format(type(value)))

        if not value.strip():
            raise ValueError('Empty string provided as status')

        return value


class WeekdayStr(StrictNonEmptyStr):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise ValueError('Invalid `type`: str expected, `{}` provided'.format(type(value)))

        if re.match(pattern=WEEKDAY_REGEX, string=value.strip(), flags=re.IGNORECASE) is None:
            raise ValueError('Invalid `type` provided for opening hours')

        return value


def strings_are_equal(first: str, second: str, case_insensitive: bool = True) -> bool:
    if not isinstance(first, str) or not isinstance(second, str):
        raise TypeError('Invalid argument provided: `str` expected')

    if case_insensitive is True:
        return first.lower() == second.lower()

    return first == second


def strings_are_not_equal(first: str, second: str, case_insensitive: bool = True) -> bool:
    return not strings_are_equal(first=first, second=second, case_insensitive=case_insensitive)
