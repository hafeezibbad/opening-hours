from typing import Union, Tuple, Optional

from src.app.models.errors import ApiError


class AppErrorType:
    # internal error code, HTTP status code, log event name
    NO_ERROR = (0, 200, 'OK')
    INTERNAL_SERVER_ERROR = (1, 500, 'INTERNAL_SERVER_ERROR')
    DATA_PARSING_FAILED = (2, 500, 'DATA_PARSING_FAILED')
    SERVICE_UNAVAILABLE_ERROR = (3, 503, 'SERVICE_UNAVAILABLE_ERROR')
    REQUEST_BODY_EMPTY = (4, 400, 'REQUEST_BODY_EMPTY')
    REQUEST_BODY_INVALID_JSON = (5, 400, 'REQUEST_BODY_INVALID_JSON')
    DATA_RETRIEVAL_FAILED = (6, 503, 'DATA_RETRIEVAL_FAILED')
    INVALID_REQUEST_DATA = (7, 400, 'INVALID_REQUEST_DATA')
    CANNOT_PARSE_OPENING_HOURS = (8, 400, 'CANNOT_PARSE_OPENING_HOURS')


class AppError(Exception):
    code: Tuple = None
    http_status: int = None
    event_name: str = None

    def __init__(self, code: Tuple) -> None:
        self.code, self.http_status, self.event_name = code


class AppSimpleError(AppError):
    """For simple errors where message and status code is enough"""
    message: str = None

    def __init__(self, code: Tuple, message: str) -> None:
        super(AppSimpleError, self).__init__(code)
        self.message = message


class AppApiError(AppError):
    """For more complex API errors raised from validation failures"""
    api_error: ApiError = None

    def __init__(self, code: Tuple, api_error: ApiError) -> None:
        super(AppApiError, self).__init__(code)
        self.api_error = api_error


class DataParsingError(AppError):
    def __init__(
            self,
            title: str,
            detail: str,
            source: Optional[Union[list, dict]] = None,
            code: Tuple = AppErrorType.CANNOT_PARSE_OPENING_HOURS
    ) -> None:
        super(DataParsingError, self).__init__(code)
        self.title = title
        self.detail = detail
        self.source = source

    def __repr__(self):
        return self.detail

    def to_json(self):
        return {
            'errors': [
                {
                    'title': self.title,
                    'detail': self.detail,
                    'source': self.source
                }
            ]
        }
