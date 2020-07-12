import json
from json.decoder import JSONDecodeError
from typing import Type, Union

from src.app.errors import AppErrorType, AppSimpleError, AppApiError
from src.app.models.common import Model
from src.app.models.status import Status

from src.app.request_parser.data_parser import RequestDataParser
from src.app.request_parser.opening_hours_data_parser import OpeningHoursDataParser
from src.app.service.health_check import HealthCheckService
from src.app.service.opening_hours import OpeningHoursService


class AppManager:
    def __init__(self):
        self.opening_hours_service = OpeningHoursService()

    def get_human_readable_opening_hours(self, request_data: dict) -> str:
        opening_hours = self.parse_request_data(parser=OpeningHoursDataParser, request_data=request_data)

        return self.opening_hours_service.get_human_readable_opening_hours(opening_hours=opening_hours)

    def parse_request_data(self, parser: Type[RequestDataParser], request_data: dict) -> Type[Model]:
        req_parser = parser(request_data=request_data)
        if not req_parser.is_valid():
            raise AppApiError(
                code=AppErrorType.INVALID_REQUEST_DATA,
                api_error=req_parser.get_api_error()
            )

        return req_parser.get_model()

    def parse_request_data_as_json(self, request_data: Union[bytes, dict]) -> dict:
        if not request_data:
            raise AppSimpleError(
                code=AppErrorType.REQUEST_BODY_EMPTY,
                message='No JSON data provided in request body'
            )

        try:
            return json.loads(request_data)
        except JSONDecodeError:
            raise AppSimpleError(
                code=AppErrorType.REQUEST_BODY_INVALID_JSON,
                message='Invalid JSON format provided in request body'
            )

    def status(self) -> Status:
        health_service = HealthCheckService()
        health_status = health_service.check_all()
        if health_status is False:
            return Status(
                message="Service is down",
                status="down",
                statusCode=503
            )

        return Status(
            message="Service is up",
            status="ok",
            statusCode=200
        )
