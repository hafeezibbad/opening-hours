from pydantic import ValidationError

from src.request_parser.data_parser import RequestDataParser


class OpeningHoursDataParser(RequestDataParser):
    def __init__(self, request_data: dict) -> None:
        super(OpeningHoursDataParser, self).__init__(request_data)
        self.__validate(data=request_data)

    def get_model(self):
        return self.model

    def __validate(self, data: dict):
        try:
            self.model = Song(**data)

        except ValidationError as ex:
            self.api_error = self._handle_pydantic_validation_error(ex)
