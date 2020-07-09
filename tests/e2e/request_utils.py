from typing import Optional, Dict, Any

# pylint: disable=no-name-in-module, C0326
from pydantic import constr

from src.lib.http_utils.api_request import E2EApiRequest
from src.lib.http_utils.request_utils import handle_api_request
from src.lib.request_id.validator import REQUEST_ID_PATTERN
from tests.e2e.common import ENDPOINT_BASE_URL
from tests.e2e.e2e_response import E2EApiResponse
from tests.fixtures.common import TEST_USER_AGENT


def get_service_status_request(
        base_url: str = ENDPOINT_BASE_URL,
        request_id: Optional[constr(regex=REQUEST_ID_PATTERN)] = None,
        user_agent: Optional[str] = TEST_USER_AGENT
):
    requester = E2EApiRequest(
        base_url=base_url,
        user_agent=user_agent,
        request_handler=handle_api_request,
        expected_response=E2EApiResponse,
        request_id=request_id
    )

    return requester.make_request(
        method='GET',
        path='/api/status'
    )


def post_song_rating_request(
        base_url: str = ENDPOINT_BASE_URL,
        request_id: Optional[constr(regex=REQUEST_ID_PATTERN)] = None,
        user_agent: Optional[str] = TEST_USER_AGENT,
        params: Optional[Dict[str, Any]] = None
):

    requester = E2EApiRequest(
        base_url=base_url,
        user_agent=user_agent,
        request_handler=handle_api_request,
        expected_response=E2EApiResponse,
        request_id=request_id
    )

    return requester.make_request(
        method='POST',
        path='/api/v1/songs/opening-hours',
        params=params
    )
