import json

from src.app.models.opening_hours import OpeningHours
from tests.fixtures.opening_hours_model_data import VALID_OPENING_HOURS

TEST_USER_AGENT = "python-requests tests/opening-hours"
REQUEST_ID_STARTS_WITH = "0000-"
REQUEST_ID_LENGTH = 37
VALID_JSON_STRING = json.dumps({"key": "value"})
VALID_HUMAN_READABLE_OPENING_HOURS = "Monday: 8 AM - 6 PM"
VALID_REQUEST_DATA = {"monday": [{"type": "open", "value": 28800}, {"type": "close", "value": 64800}]}
VALID_PARSED_OPENING_HOURS = {"monday": ["8 AM - 6 PM"]}
VALID_OPENING_HOURS_OBJ = OpeningHours.load(VALID_OPENING_HOURS[0][0])
PARSED_OPENING_HOURS_DATA = [
    (
        {
            "friday": [{
                "type": "open",
                "value": 61200
            }],
            "saturday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 28800
                },
                {
                    "type": "close",
                    "value": 36000
                },
                {
                    "type": "open",
                    "value": 54000
                },
                {
                    "type": "close",
                    "value": 79200
                }
            ]
        },
        {'friday': ['5 PM - 1 AM'], 'saturday': ['8 AM - 10 AM', '3 PM - 10 PM']}
    ),
    (
        {
            "monday": [],
            "tuesday": [
                {
                    "type": "open",
                    "value": 36000
                },
                {
                    "type": "close",
                    "value": 64800
                }
            ]
        },
        {'monday': [], 'tuesday': ['10 AM - 6 PM']}
    )
]
