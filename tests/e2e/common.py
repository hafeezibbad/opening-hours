import os
import copy
from typing import List
import pytest

from src.lib.request_id.validator import RequestIdValidator

ENDPOINT_BASE_URL = os.environ["ENDPOINT_BASE_URL"]


@pytest.fixture
def fixture_request_id():
    return RequestIdValidator.generate()


def invalidate_song_data(song_data: dict, invalid_field_names: List[str], invalid_values: List[str]) -> dict:
    invalid_song_data = copy.deepcopy(song_data)
    for i, _ in enumerate(invalid_field_names):
        invalid_song_data[invalid_field_names[i]] = invalid_values[i]

    return invalid_song_data
