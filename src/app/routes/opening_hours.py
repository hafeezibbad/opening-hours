from flask import Blueprint, request

from src.app.errors import AppError, DataParsingError
from src.lib.errors.exceptions import handle_and_log_service_exception, handle_and_log_unknown_exception
from src.lib.logging.utils import log_request
from src.lib.response.utils import create_response_and_log

from src.app.routes.common import create_app_manager

# pylint: disable=invalid-name
opening_hours_api = Blueprint('', __name__)
OPENING_HOURS_API_PREFIX = '/api/v1'


@opening_hours_api.route('/opening-hours', methods=['POST'])
def parse_opening_hours():
    try:
        manager = create_app_manager(incoming_request=request)
        request_data: dict = manager.parse_request_data_as_json(request.get_data())
        log_request(log_message="Opening hour parsing started", log_data=True, request_data=request_data)

        parsed_hours: str = manager.get_human_readable_opening_hours(request_data=request_data)

        return create_response_and_log(
            log_message='Opening hours parsing successful',
            message='Opening hours parsing successful',
            log_data=True,
            data=parsed_hours,
            status_code=200,
            content_type='text'
        )

    except DataParsingError as ex:
        return handle_and_log_service_exception(
            ex,
            service_name="Opening hours app",
            message="Opening hours parsing failed"
        )

    except AppError as ex:
        return handle_and_log_service_exception(
            ex,
            service_name="Opening hours App",
            message='Opening hours parsing failed'
        )

    except BaseException as ex:
        return handle_and_log_unknown_exception(ex, message='Unknown exception')
