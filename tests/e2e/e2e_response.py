import json
from typing import Union, Optional

from src.lib.errors.api_errors import ApiErrorAssertions
from src.lib.errors.data_parsing_errors import DataParsingErrorAssertions
from src.lib.http_utils.http_response import HttpResponse


class E2EApiResponse(HttpResponse):
    def __init__(self, response: dict):
        self.response: dict = response
        self.headers: dict = response["headers"]
        self.status_code: int = response["statusCode"]
        self.body_parsed: bool = False
        self.body: Union[dict, str] = {}
        self.api_error: Optional[ApiErrorAssertions] = None
        self.parsing_errors: Optional[DataParsingErrorAssertions] = None

    def _parse_body(self):
        if self.body_parsed is True:
            return

        if not self.response.get('body'):
            self.body = dict()
            return

        if self.headers.get('Content-Type') == 'application/json':
            self.body = json.loads(self.response['body'])
            self.api_error = ApiErrorAssertions(self.body)
            self.parsing_errors = DataParsingErrorAssertions(self.body)

        elif self.headers.get('Content-Type') == 'text/html; charset=utf-8':
            self.body = self.response['body']

        self.body_parsed = True

    def validation_error_count_is(self, count: int):
        self._parse_body()
        self.api_error.error_count_is(count)

    def has_one_validation_error(self):
        self.validation_error_count_is(1)

    def validation_error_title_is(self, title: str):
        self._parse_body()
        assert self.body['errors'][0]['title'] == title

    def validation_error_detail_is(self, details: str):
        self._parse_body()
        assert self.body['errors'][0]['detail'] == details

    def has_validation_error_with_title(self, title: str):
        self._parse_body()
        self.api_error.has_validation_error_with_title(title)

    def has_validation_error_with_title_and_detail(self, title: str, detail: str):
        self._parse_body()
        self.api_error.has_validation_error_with_title_and_detail(title, detail)

    def has_parsing_error_with_title(self, title: str):
        self._parse_body()
        assert self.body[0]['title'] == title

    def has_parsing_error_with_details(self, detail: str):
        self._parse_body()
        assert self.body[0]['detail'] == detail

    def has_parsing_error_with_title_and_details(self, title: str, detail: str):
        self._parse_body()
        self.parsing_errors.has_parsing_error_with_title_and_detail(title=title, detail=detail)
