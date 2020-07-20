from typing import Optional, Any, Dict
import sys
import traceback

from flask import request, g

from src.app.errors import DataParsingError
from src.lib.logging.utils import LOGGING
from src.lib.response.utils import create_json_response
from src.app.models.errors import ApiError


# pylint: disable=C0326
class GenericErrorType:
    INTERNAL_SERVER_ERROR = (1, 500, 'INTERNAL_SERVER_ERROR')


class GenericError(Exception):
    http_status: int
    code: int
    event_name: str
    message: str
    verbose_message: Optional[str] = None  # Verbose message that is only logged, not shown to end user

    def __init__(self, message: str, error_type: tuple, verbose_message: Optional[str] = None):
        self.message = message
        self.code, self.http_status, self.event_name = error_type
        self.verbose_message = verbose_message


def get_exception_details(ex) -> Dict[str, Any]:
    ex_type, ex_value, ex_traceback = sys.exc_info()    # provides info for most recent (if any) by default

    traceback_out = traceback.format_exc()

    traceback_details: dict = {}
    if ex_type:
        traceback_details.update({'type': ex_type.__name__})
    if ex_traceback:
        traceback_details.update({
            'filename': ex_traceback.tb_frame.f_code.co_filename,
            'lineno': ex_traceback.tb_lineno,
            'name': ex_traceback.tb_frame.f_code.co_name
        })

    ex_message = str(ex)
    if hasattr(ex, 'message'):
        ex_message = ex.message

    exception_details = {
        'exception_class': str(ex.__class__.__name__),
        'exception_message': ex_message,
        'exception_traceback_details': traceback_details,
        'exception_traceback': str(traceback_out)
    }

    return exception_details


def handle_and_log_flask_exception(ex, exception_details: bool = True):
    exceptional_trace: Optional[Dict[str, Any]] = None
    if exception_details is True:
        exceptional_trace = get_exception_details(ex)

    http_status = ex.code or 500
    message = ex.name

    LOGGING.error(
        'FLASK_EXCEPTION',
        request_type=request.method,
        request_path=request.path,
        message="Flask HTTP exception",
        status_code=http_status,
        exception_details=exceptional_trace,
        request_id=g.request_id
    )

    return create_json_response(message=message, status_code=http_status)


def handle_and_log_unknown_exception(ex, message: str = 'Unknown exception'):
    exception_details = get_exception_details(ex)
    http_status = 500

    LOGGING.fatal(
        'UNKNOWN_EXCEPTION',
        request_method=request.method.lower(),
        request_path=request.path,
        message=message,
        response_status_code=http_status,
        exception_details=exception_details,
        request_id=g.request_id
    )

    return create_json_response(message='Internal server error', status_code=http_status)


def handle_and_log_service_exception(ex, service_name: str = "SERVICE", message: str = "Service error"):
    exception_details = get_exception_details(ex)
    http_status = 500
    error_message = message
    verbose_message = None

    data = dict()
    if hasattr(ex, 'http_status'):
        http_status = ex.http_status

    if hasattr(ex, 'message'):
        error_message = ex.message
    if hasattr(ex, 'verbose_message'):
        verbose_message = ex.verbose_message

    LOGGING.error(
        '{}_ERROR'.format(service_name.upper()),
        message=error_message,
        verbose_message=verbose_message,
        request_method=request.method.lower(),
        request_path=request.path,
        response_status_code=http_status,
        exception_details=exception_details,
        request_id=g.request_id
    )

    if isinstance(ex, DataParsingError):
        data = ex.to_json()

    if hasattr(ex, 'api_error') and isinstance(ex.api_error, ApiError):
        data = ex.api_error.dict()

    return create_json_response(message=error_message, status_code=http_status, data=data)


def handle_configuration_exception(ex, message: str = 'error'):
    exception_details = get_exception_details(ex)
    http_status = 500
    if hasattr(ex, 'http_status'):
        http_status = ex.http_status

    LOGGING.error(
        'CONFIGURATION_ERROR',
        message=message,
        request_method=request.method.lower(),
        request_path=request.path,
        response_status_code=http_status,
        exception_details=exception_details
    )

    return create_json_response(message=message, status_code=http_status)
