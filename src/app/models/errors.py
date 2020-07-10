from typing import Optional, List

from src.app.models.common import Model
from src.lib.configuration.validate import StrictNonEmptyStr


class ErrorPointer(Model):
    pointer: Optional[str] = None


class Error(Model):
    status: int
    title: StrictNonEmptyStr
    detail: Optional[str] = None
    source: Optional[ErrorPointer] = None


class ApiError(Model):
    errors: List[Error]


class ParsingErrorPointer(Model):
    day: StrictNonEmptyStr
    event: StrictNonEmptyStr


class ParsingError(Model):
    title: StrictNonEmptyStr
    detail: Optional[str] = None
    source: Optional[dict] = None
