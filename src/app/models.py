from typing import List, Optional

from pydantic import BaseModel, conint  # pylint: disable=no-name-in-module
from typing_extensions import Literal

from src.lib.configuration.validate import StrictNonEmptyStr


class Model(BaseModel):
    @classmethod
    def load(cls, data: dict, **kwargs):
        init = {}
        for k, v in data.items():
            if k.lower() == "type":
                k = "entry_type"  # FIXME: This is an ugly hack to load TimingEntry objects
            if k in cls.schema()["properties"]:
                init[k] = v

        if init:
            return cls(**init, **kwargs)  # type: ignore

        raise ValueError(init)


class TimingEntry(Model):
    entry_type: Literal["open", "close"]
    value: conint(ge=0, le=86400)


class DayTiming(Model):
    timings: List[TimingEntry]


class OpeningHours(Model):
    monday: DayTiming
    tuesday: DayTiming
    wednesday: DayTiming
    thursday: DayTiming
    friday: DayTiming
    saturday: DayTiming
    sunday: DayTiming

    @property
    def day_sequence(self):
        return [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday, self.sunday]


class ErrorPointer(Model):
    pointer: Optional[str] = None


class Error(Model):
    status: int
    title: StrictNonEmptyStr
    detail: Optional[str] = None
    source: Optional[ErrorPointer] = None


class ApiError(Model):
    errors: List[Error]


class Status(Model):
    message: str
    status: str
    statusCode: Literal[200, 503]

    def get_status_data(self):
        fields: dict = self.dict()
        del fields['statusCode']

        return fields
