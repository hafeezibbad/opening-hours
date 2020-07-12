VALID_OPENING_HOURS = [
    (
        {
            "friday": [{
                "type": "open",
                "value": 64800
            }],
            "saturday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 32400
                },
                {
                    "type": "close",
                    "value": 39600
                },
                {
                    "type": "open",
                    "value": 57600
                },
                {
                    "type": "close",
                    "value": 82800
                }
            ]
        },
        '\n'.join(['Friday: 6 PM - 1 AM', 'Saturday: 9 AM - 11 AM, 4 PM - 11 PM'])
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
            ],
            "wednesday": [],
            "thursday": [
                {
                    "type": "open",
                    "value": 36000
                },
                {
                    "type": "close",
                    "value": 64800
                }
            ],
            "friday": [
                {
                    "type": "open",
                    "value": 36000
                }
            ],
            "saturday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 36000
                }
            ],
            "sunday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 43200
                },
                {
                    "type": "close",
                    "value": 75600
                }
            ]
        },
        '\n'.join([
            'Monday: Closed',
            'Tuesday: 10 AM - 6 PM',
            'Wednesday: Closed',
            'Thursday: 10 AM - 6 PM',
            'Friday: 10 AM - 1 AM',
            'Saturday: 10 AM - 1 AM',
            'Sunday: 12 PM - 9 PM'
        ])
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
            ],
            "wednesday": [],
        },
        '\n'.join(['Monday: Closed', 'Tuesday: 10 AM - 6 PM', 'Wednesday: Closed'])
    ),
    (
        {
            "friday": [
                {
                    "type": "open",
                    "value": 35817
                }
            ],
            "saturday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 27303
                },
                {
                    "type": "close",
                    "value": 30380
                },
                {
                    "type": "open",
                    "value": 56310
                },
                {
                    "type": "close",
                    "value": 61630
                }
            ]
        },
        '\n'.join(['Friday: 9:56:57 AM - 1 AM', 'Saturday: 7:35:03 AM - 8:26:20 AM, 3:38:30 PM - 5:07:10 PM'])
    ),
    (
        {
            "monday": [
                {
                    "type": "open",
                    "value": 54000
                },
                {
                    "type": "close",
                    "value": 61200
                }
            ],
            "tuesday": [
                {
                    "type": "open",
                    "value": 54000
                },
                {
                    "type": "close",
                    "value": 61200
                }
            ],
            "wednesday": [
                {
                    "type": "open",
                    "value": 54000
                },
                {
                    "type": "close",
                    "value": 61200
                }
            ],
            "thursday": [
                {
                    "type": "open",
                    "value": 54000
                },
                {
                    "type": "close",
                    "value": 61200
                }
            ],
            "friday": [
                {
                    "type": "open",
                    "value": 54000
                },
                {
                    "type": "close",
                    "value": 61200
                }
            ],
            "saturday": [
                {
                    "type": "open",
                    "value": 54000
                },
                {
                    "type": "close",
                    "value": 61200
                }
            ],
            "sunday": [
                {
                    "type": "open",
                    "value": 54000
                },
                {
                    "type": "close",
                    "value": 61200
                }
            ]
        },
        '\n'.join([
            'Monday: 3 PM - 5 PM',
            'Tuesday: 3 PM - 5 PM',
            'Wednesday: 3 PM - 5 PM',
            'Thursday: 3 PM - 5 PM',
            'Friday: 3 PM - 5 PM',
            'Saturday: 3 PM - 5 PM',
            'Sunday: 3 PM - 5 PM'
        ])
    ),
    (
        {
            "sunday": [
                {
                    "type": "open",
                    "value": 54000
                },
                {
                    "type": "close",
                    "value": 61200
                },
                {
                    "type": "open",
                    "value": "72000"
                }
            ]
        },
        "Sunday: 3 PM - 5 PM, 8 PM -"
    )
]

VALID_OPENING_HOURS_TEXT_CASE_VARIATIONS = [
    (
        {
            "friday": [
                {  # lowercase
                    "type": "open",
                    "value": 64800
                }
            ],
            "SATURDAY": [
                {  # uppercase
                    "TYPE": "close",
                    "VALUE": 3600
                }
            ]
        },
        '\n'.join(['Friday: 6 PM - 1 AM', 'Saturday: Closed'])
    ),
    (
        {
            "friDay": [
                {    # CamelCase
                    "typE": "open",
                    "valuE": 64800
                }
            ],
            "Saturday": [
                {  # title-case
                    "Type": "close",
                    "Value": 3600
                }
            ]
        },
        '\n'.join(['Friday: 6 PM - 1 AM', 'Saturday: Closed'])
    )
]

OPENING_TIMES_WITH_SINGLE_VALIDATION_ERROR = [
    (
        {
            "friday": [
                {
                    "type": "invalid_type",
                    "value": 64800
                }, {
                    "type": "close",
                    "value": 64800
                }
            ]
        },
        "Input validation failed",
        "Invalid `type`. Choices are `open, close`"
    ),
    (
        {
            "saturday": [
                {
                    "type": "open",
                    "value": 99999
                }, {
                    "type": "close",
                    "value": 64800
                }
            ]
        },
        "Input validation failed",
        "Invalid data for value",
    ),
    (
        {
            "sunday": [
                {
                    "type": "open",
                    "value": -1
                }, {
                    "type": "close",
                    "value": 64800
                }
            ]
        },
        "Input validation failed",
        "Invalid data for value",
    ),
    (
        {
            "friday": [
                {
                    "type": "open",
                    "value": 1
                }, {
                    "type": "close",
                    "value": 86400
                }
            ]
        },
        "Input validation failed",
        "Invalid data for value",
    )
]

OPENING_HOURS_WITH_NO_CLOSING_TIME = [
    (
        {
            "monday": [
                {
                    "type": "open",
                    "value": 32400
                }
            ],
            "tuesday": [
                {
                    "type": "open",
                    "value": 14400
                },
                {
                    "type": "close",
                    "value": 32000
                }
            ]
        },
        "Missing closing times",
        "`Monday: 9 AM` has no closing time"
    ),
    (
        {
            "tuesday": [
                {
                    "type": "open",
                    "value": 33600
                },
                {
                    "type": "close",
                    "value": 43600
                }
            ],
            "wednesday": [],
            "friday": [
                {
                    "type": "open",
                    "value": 57600
                }
            ]
        },
        "Missing closing time",
        "`Friday: 4 PM` has no closing time"
    ),
    (
        {
            "friday": [
                {
                    "type": "open",
                    "value": 57600
                }
            ],
            "sunday": [
                {
                    "type": "open",
                    "value": 82800
                }
            ]
        },
        "Missing closing time",
        "`Friday: 4 PM` has no closing time on following day",
    ),
    (
        {
            "monday": [],
            "tuesday": [
                {
                    "type": "open",
                    "value": 3600
                }
            ],
            "friday": [
                {
                    "type": "open",
                    "value": 57600
                }
            ],
            "sunday": [
                {
                    "type": "open",
                    "value": 82800
                }
            ]
        },
        "Missing closing time",
        "`Tuesday: 1 AM` has no closing time on following day",
    ),
    (
        {
            "tuesday": [
                {
                    "type": "open",
                    "value": 33600
                },
                {
                    "type": "close",
                    "value": 43600
                },
                {
                    "type": "open",
                    "value": 53600
                }
            ],
            "wednesday": [],
            "friday": [
                {
                    "type": "open",
                    "value": 57600
                }
            ]
        },
        "Missing closing time",
        "`Tuesday: 2:53:20 PM` has no closing time on following day"
    ),
    (
        {
            "monday": [
                {
                    "type": "open",
                    "value": 43201
                }
            ],
            "tuesday": [
                {
                    "type": "open",
                    "value": 123
                }
            ]
        },
        "Missing closing times",
        "`Monday: 12:00:01 PM` has no closing time"
    ),
    (
        {
            "monday": [
                {
                    "type": "open",
                    "value": 43201
                },
                {
                    "type": "close",
                    "value": 50400
                },
                {
                    "type": "open",
                    "value": 58200
                }

            ],
            "tuesday": [
                {
                    "type": "open",
                    "value": 123
                }
            ]
        },
        "Missing closing times",
        "`Monday: 4:10 PM` has no closing time"
    ),
    (
        {
            "monday": [
                {
                    "type": "open",
                    "value": 32400
                }
            ],
            "tuesday": [
                {
                    "type": "close",
                    "value": 32400
                },
                {
                    "type": "open",
                    "value": 64800
                }
            ]
        },
        "Missing closing time",
        "`Tuesday: 6 PM` has no closing time"
    ),
    (
        {
            "monday": [
                {
                    "type": "open",
                    "value": 32400
                }
            ],
            "tuesday": [
                {
                    "type": "open",
                    "value": 32400
                },
                {
                    "type": "close",
                    "value": 32000
                }
            ]
        },
        "Missing closing time",
        "`Tuesday: 9 AM` has no closing time"
    )
]

CLOSING_HOURS_WITH_NO_OPENING_TIME = [
    (
        {
            "monday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 32400
                },
                {
                    "type": "close",
                    "value": 61200
                }
            ],
            "tuesday": [
                {
                    "type": "close",
                    "value": 3600
                }
            ]
        },
        "Missing opening times",
        "`Tuesday: 1 AM` has no opening time"
    ),
    (
        {
            "monday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 32400
                },
                {
                    "type": "close",
                    "value": 61200
                }
            ],
            "tuesday": [],
            "wednesday": [
                {
                    "type": "close",
                    "value": 3600
                }
            ]
        },
        "Missing opening times",
        "`Wednesday: 1 AM` has no opening time",
    ),
    (
        {
            "monday": [
                {
                    "type": "open",
                    "value": 32400
                },
                {
                    "type": "close",
                    "value": 61200
                },
                {
                    "type": "close",
                    "value": 64800
                }
            ]
        },
        "Invalid event sequence",
        "Overlapping intervals or consecutive events of same `type`",
    )
]

OPENING_HOURS_CLOSING_DAYS = [
    # All days are closed
    (
        {
            "monday": [],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [],
            "saturday": [],
            "sunday": []
        },
        '\n'.join([
            'Monday: Closed',
            'Tuesday: Closed',
            'Wednesday: Closed',
            'Thursday: Closed',
            'Friday: Closed',
            'Saturday: Closed',
            'Sunday: Closed'
        ])
    ),
    # Only those days are closed where data for day is empty list
    (
        {
            "wednesday": [],
            "thursday": [],
            "saturday": []
        },
        '\n'.join([
            'Wednesday: Closed',
            'Thursday: Closed',
            'Saturday: Closed',
        ])
    )
]

OPENING_HOURS_WITH_CONSECUTIVE_SIMILAR_INTERVALS = [
    # Consecutive open intervals (based on sorted `value`, i.e. time)
    # This is case for overlapping open interval
    (
        {
            "monday": [
                {
                    "type": "open",
                    "value": 3600
                },
                {
                    "type": "close",
                    "value": 43200
                },
                {
                    "type": "open",
                    "value": 25200
                },
                {
                    "type": "open",
                    "value": 61200
                }
            ]
        },
        "Invalid event sequence",
        "Overlapping intervals or consecutive events of same `type`"
    ),
    # Consecutive close intervals without an open interval in between
    (
        {
            "monday": [
                {
                    "type": "open",
                    "value": 3600
                },
                {
                    "type": "close",
                    "value": 43200
                },
                {
                    "type": "open",
                    "value": 61200
                },
                {
                    "type": "close",
                    "value": 25200
                }
            ]
        },
        "Invalid event sequence",
        "Overlapping intervals or consecutive events of same `type`",
    )
]

OPENING_HOURS_INVALID_SEQUENCE = [
    # Closing time is before opening time
    (
        {
            "monday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 43200
                }
            ]
        },
        "Missing closing time",
        "`Monday: 12 PM` has no closing time"
    ),
    # Closing time is before opening time on Tuesday, with no times on Monday or wednesday
    (
        {
            "monday": [],
            "tuesday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 43200
                }
            ],
            "wednesday": []
        },
        "Missing closing time",
        "`Tuesday: 12 PM` has no closing time"
    )
]

OPENING_HOURS_WHEN_FIRST_EVENT_IN_WEEK_IS_CLOSE = [
    (
        {
            "monday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 32400
                },
                {
                    "type": "close",
                    "value": 61200
                }
            ]
        },
        'Monday: 9 AM - 5 PM'
    ),
    (
        {
            "monday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 32400
                }
            ],
            "tuesday": [
                {
                    "type": "close",
                    "value": 32000
                }
            ]
        },
        '\n'.join(['Monday: 9 AM - 8:53:20 AM', 'Tuesday: Closed'])
    ),
    (
        {
            "tuesday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 32400
                }
            ],
            "wednesday": [
                {
                    "type": "close",
                    "value": 32000
                }
            ]
        },
        '\n'.join(['Tuesday: 9 AM - 8:53:20 AM', 'Wednesday: Closed'])
    ),
    (
        {
            "monday": [],
            "tuesday": [
                {
                    "type": "close",
                    "value": 3600
                },
                {
                    "type": "open",
                    "value": 32400
                }
            ],
            "wednesday": [
                {
                    "type": "close",
                    "value": 32000
                }
            ]
        },
        '\n'.join(['Monday: Closed', 'Tuesday: 9 AM - 8:53:20 AM', 'Wednesday: Closed'])
    )
]
