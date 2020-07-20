import json
from typing import Optional, Dict, Any, Union

from flask import request, Response
from typing_extensions import Literal

from src.app.models.opening_hours import TimeEntry, DayTimings, OpeningHours
from src.lib.logging.utils import LOGGING


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=W0221, E0202
        if isinstance(obj, (TimeEntry, DayTimings)):
            return obj.dict()

        if isinstance(obj, OpeningHours):
            return {k: v for k, v in obj.dict().items() if v.get('timings') is not None}

        return json.JSONEncoder.default(self, obj)


def create_json_response(
        message: Optional[str] = None,
        status_code: int = 200,
        data: Optional[dict] = None,
        extra_headers: Optional[Dict[str, Any]] = None,
) -> Response:
    data = data or dict()
    if message:
        data['message'] = message

    js = json.dumps(data, cls=CustomJsonEncoder)

    response = Response(
        js,
        status=status_code,
        mimetype='application/json'
    )
    if extra_headers:
        for k, v in extra_headers.items():
            response.headers[k] = v

    return response


def create_text_response(
        data: Union[str, dict] = '',
        extra_headers: Optional[Dict[str, Any]] = None,
        status_code: int = 200
) -> Response:
    response = Response(
        data,
        status=status_code
    )
    if extra_headers:
        for k, v in extra_headers.items():
            response.headers[k] = v

    return response


def create_response_and_log(
        log_message: str,
        message: Optional[str] = None,
        status_code: int = 200,
        data: Optional[dict] = None,
        log_data: bool = False,
        extra_headers: Optional[Dict[str, Any]] = None,
        content_type: Literal['text', 'json'] = 'json'
):
    data = data or dict()
    response_data = None

    if log_data is True:
        response_data = data

    LOGGING.info(
        'HTTP_RESPONSE',
        message=log_message,
        request_method=request.method,
        request_path=request.path,
        response_status_code=status_code,
        response_data=response_data,
        response_extra_headers=extra_headers
    )

    if content_type.lower() == 'text':
        return create_text_response(data=data, extra_headers=extra_headers)

    return create_json_response(message=message, status_code=status_code, data=data, extra_headers=extra_headers)
