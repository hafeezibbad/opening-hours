from werkzeug.wrappers import Response

# pylint: disable=no-name-in-module
from src.lib.http_utils.http_response import HttpResponse


# pylint: disable=W0201
class FlaskApiResponse(HttpResponse):
    def __init__(self, response: Response):
        self.response = response
        self.headers = response.headers
        self.status_code = response.status_code
        self.raw_body = str(response.data)
        self.body_parsed = False
        self.body = {}

    def _parse_body(self):
        if self.body_parsed is True:
            return

        if len(self.response.data) == 0:
            self.body = dict()
            return

        self.body = self.response.json
        self.body_parsed = True
