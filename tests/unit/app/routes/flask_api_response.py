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

        if self.headers.get('Content-Type') == 'application/json':
            self.body = self.response.json

        elif self.headers.get('Content-Type') == 'text/html; charset=utf-8':
            self.body = self.response.data.decode('utf-8')

        self.body_parsed = True
