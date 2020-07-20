import json
from abc import ABC, abstractmethod
from typing import Type, Dict, List, Optional, Any

from pydantic import ValidationError

from src.app.models.common import Model
from src.app.models.errors import ApiError


class RequestDataParserABC(ABC):
    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_api_error(self) -> Optional[ApiError]:
        pass

    @abstractmethod
    def get_model(self) -> Type[Model]:
        pass


class RequestDataParser(RequestDataParserABC):
    def __init__(self, request_data: dict) -> None:
        self.errors: List[Dict[str, Any]] = []
        self.model: Optional[Model] = None
        self.api_error: Optional[ApiError] = None
        self.request_data = request_data

    def get_api_error(self) -> Optional[ApiError]:
        return self.api_error

    def is_valid(self):
        return not self.errors

    def get_model(self) -> Type[Model]:
        raise NotImplementedError

    def _handle_pydantic_validation_error(
            self,
            validation_error: ValidationError,
            overridden_field_names: Dict[str, str]
    ) -> ApiError:
        errors = []
        errors_dict = json.loads(validation_error.json())

        for error in errors_dict:
            status = 400  # Data validation failure: 400 Bad Request

            field_name = error['loc'][0]
            if field_name in overridden_field_names:
                field_name = overridden_field_names.get(field_name)

            error_title = 'Input validation failed'
            if error.get('type', '').lower() == 'value_error':
                error_detail = error['msg']
            else:
                error_detail = 'Invalid data for {field_name}'.format(field_name=field_name)

            api_error_dict = {
                'status': status,
                'source': {
                    'pointer': field_name
                },
                'title': error_title,
                'detail': error_detail
            }

            errors.append(api_error_dict)
        self.errors = errors

        return ApiError(**{'errors': errors})
