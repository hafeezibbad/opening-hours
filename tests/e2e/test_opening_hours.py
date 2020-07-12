import pytest
from pydantic import constr  # pylint: disable=no-name-in-module

from src.lib.request_id.validator import REQUEST_ID_PATTERN
from tests.e2e.common import fixture_request_id  # pylint: disable=unused-import
from tests.e2e.e2e_response import E2EApiResponse
from tests.e2e.request_utils import post_opening_hours_request
from tests.fixtures.opening_hours_data import VALID_OPENING_HOURS, OPENING_TIMES_WITH_SINGLE_VALIDATION_ERROR, \
    VALID_OPENING_HOURS_TEXT_CASE_VARIATIONS, OPENING_HOURS_WITH_NO_CLOSING_TIME, OPENING_HOURS_CLOSING_DAYS, \
    OPENING_HOURS_WITH_CONSECUTIVE_SIMILAR_INTERVALS, OPENING_HOURS_INVALID_SEQUENCE, \
    OPENING_HOURS_WHEN_FIRST_EVENT_IN_WEEK_IS_CLOSE, CLOSING_HOURS_WITH_NO_OPENING_TIME


# pylint: disable=redefined-outer-name
class TestPostOpeningHours:
    @pytest.mark.parametrize('request_data,expected_response', VALID_OPENING_HOURS)
    def test_opening_hours_response_is_ok(
            self,
            request_data: dict,
            expected_response: str,
            fixture_request_id: constr(regex=REQUEST_ID_PATTERN)
    ):
        response: E2EApiResponse = post_opening_hours_request(request_id=fixture_request_id, request_data=request_data)

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        response.text_data_is(expected_response)

    @pytest.mark.parametrize('request_data,expected_response', VALID_OPENING_HOURS_TEXT_CASE_VARIATIONS)
    def test_opening_hours_response_is_ok_with_text_case(
            self,
            request_data: dict,
            expected_response: str,
            fixture_request_id: constr(regex=REQUEST_ID_PATTERN)
    ):
        response: E2EApiResponse = post_opening_hours_request(request_id=fixture_request_id, request_data=request_data)

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        response.text_data_is(expected_response)

    @pytest.mark.parametrize('request_data,error_title,error_detail', OPENING_TIMES_WITH_SINGLE_VALIDATION_ERROR)
    def test_opening_hours_raise_validation_error(
            self,
            request_data: dict,
            error_title: str,
            error_detail: str,
            fixture_request_id: constr(regex=REQUEST_ID_PATTERN)
    ):
        response: E2EApiResponse = post_opening_hours_request(request_id=fixture_request_id, request_data=request_data)

        response.status_code_is_400_bad_request()
        response.contains_request_id(fixture_request_id)
        response.has_one_validation_error()
        response.has_validation_error_with_title_and_detail(error_title, error_detail)

    @pytest.mark.parametrize('request_data,error_title,error_detail', OPENING_HOURS_WITH_NO_CLOSING_TIME)
    def test_opening_hours_when_no_closing_time_is_provided(
            self,
            request_data: dict,
            error_title: str,
            error_detail: str,
            fixture_request_id: constr(regex=REQUEST_ID_PATTERN)
    ):
        response: E2EApiResponse = post_opening_hours_request(request_id=fixture_request_id, request_data=request_data)

        response.status_code_is_400_bad_request()
        response.contains_request_id(fixture_request_id)
        response.has_parsing_error_with_title_and_details(title=error_title, detail=error_detail)

    @pytest.mark.parametrize('request_data,expected_response', OPENING_HOURS_CLOSING_DAYS)
    def test_opening_hours_for_closed_days(
            self,
            request_data: dict,
            expected_response: str,
            fixture_request_id: constr(regex=REQUEST_ID_PATTERN)
    ):
        response: E2EApiResponse = post_opening_hours_request(request_id=fixture_request_id, request_data=request_data)

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        response.text_data_is(expected_response)

    @pytest.mark.parametrize('request_data,error_title,error_detail', OPENING_HOURS_WITH_CONSECUTIVE_SIMILAR_INTERVALS)
    def test_opening_hours_for_overlapping_intervals(
            self,
            request_data: dict,
            error_title: str,
            error_detail: str,
            fixture_request_id: constr(regex=REQUEST_ID_PATTERN)
    ):
        response: E2EApiResponse = post_opening_hours_request(request_id=fixture_request_id, request_data=request_data)

        response.status_code_is_400_bad_request()
        response.contains_request_id(fixture_request_id)
        response.has_parsing_error_with_title_and_details(title=error_title, detail=error_detail)

    @pytest.mark.parametrize('request_data,error_title,error_detail', OPENING_HOURS_INVALID_SEQUENCE)
    def test_opening_hours_for_invalid_event_sequence(
            self,
            request_data: dict,
            error_title: str,
            error_detail: str,
            fixture_request_id: constr(regex=REQUEST_ID_PATTERN)
    ):
        response: E2EApiResponse = post_opening_hours_request(request_id=fixture_request_id, request_data=request_data)

        response.status_code_is_400_bad_request()
        response.contains_request_id(fixture_request_id)
        response.has_parsing_error_with_title_and_details(title=error_title, detail=error_detail)

    @pytest.mark.parametrize('request_data,expected_response', OPENING_HOURS_WHEN_FIRST_EVENT_IN_WEEK_IS_CLOSE)
    def test_opening_hours_when_first_event_of_week_is_close(
            self,
            request_data: dict,
            expected_response: str,
            fixture_request_id: constr(regex=REQUEST_ID_PATTERN)
    ):
        response: E2EApiResponse = post_opening_hours_request(request_id=fixture_request_id, request_data=request_data)

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        response.text_data_is(expected_response)

    @pytest.mark.parametrize('request_data,error_title,error_detail', CLOSING_HOURS_WITH_NO_OPENING_TIME)
    def test_opening_hours_when_opening_time_is_not_available(
            self,
            request_data: dict,
            error_title: str,
            error_detail: str,
            fixture_request_id: constr(regex=REQUEST_ID_PATTERN)
    ):
        response: E2EApiResponse = post_opening_hours_request(request_id=fixture_request_id, request_data=request_data)

        response.status_code_is_400_bad_request()
        response.contains_request_id(fixture_request_id)
        response.has_parsing_error_with_title_and_details(title=error_title, detail=error_detail)
