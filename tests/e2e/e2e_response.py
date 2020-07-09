import json
from typing import Optional

import pytest

from src.lib.errors.api_errors import ApiErrorAssertions
from src.lib.http_utils.http_response import HttpResponse


class E2EApiResponse(HttpResponse):
    def __init__(self, response: dict):
        self.response = response
        self.headers = response["headers"]
        self.status_code = response["statusCode"]
        self.body_parsed = False
        self.body = {}
        self.api_error = None

    def _parse_body(self):
        if self.body_parsed is True:
            return

        if not self.response.get('body'):
            self.body = dict()
            return

        self.body = json.loads(self.response["body"])
        self.api_error = ApiErrorAssertions(self.body)
        self.body_parsed = True
