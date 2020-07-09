import json
from json.decoder import JSONDecodeError
from typing import Optional, Type, Union

from src.app.errors import AppApiError, AppErrorType, AppSimpleError
from src.app.models import Model, Status

from src.request_parser.data_parser import RequestDataParser
from src.service.health_check import HealthCheckService


class AppManager:
    def __init__(self, requester_ip: Optional[str] = None):
        self.requester_ip = requester_ip

    def __parse_request_data(self, parser: Type[RequestDataParser], request_data: dict) -> Type[Model]:
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
