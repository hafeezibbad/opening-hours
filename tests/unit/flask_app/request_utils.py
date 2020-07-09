from typing import Optional

# pylint: disable=no-name-in-module
from src.lib.http_utils.api_request import FlaskApiRequest
from tests.fixtures.common import TEST_USER_AGENT
from tests.unit.flask_app.common import client
from tests.unit.flask_app.flask_api_response import FlaskApiResponse


def get_status_request(
        base_url: str = '',
        user_agent: str = TEST_USER_AGENT,
        request_id: Optional[str] = None
):
    requester = FlaskApiRequest(
        base_url=base_url,
        user_agent=user_agent,
        request_handler=client,
        expected_response=FlaskApiResponse,
        request_id=request_id
    )

    return requester.make_request(
        method='GET',
        path='/api/status'
    )
