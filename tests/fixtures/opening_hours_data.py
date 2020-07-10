VALID_OPENING_HOURS = [
    (
        {
            "friday": [{
                "type": "open",
                "value": 64800
            }],
            "saturday": [{
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
            "tuesday": [{
                "type": "open",
                "value": 36000
            },
                {
                    "type": "close",
                    "value": 64800
                }
            ],
            "wednesday": [],
            "thursday": [{
                "type": "open",
                "value": 36000
            },
                {
                    "type": "close",
                    "value": 64800
                }
            ],
            "friday": [{
                "type": "open",
                "value": 36000
            }],
            "saturday": [{
                "type": "close",
                "value": 3600
            },
                {
                    "type": "open",
                    "value": 36000
                }
            ],
            "sunday": [{
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
            "tuesday": [{
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
    )
]

VALID_OPENING_HOURS_TEXT_CASE_VARIATIONS = [
    (
        {
            "friday": [{  # lowercase
                "type": "open",
                "value": 64800
            }],
            "SATURDAY": [{  # uppercase
                "TYPE": "close",
                "VALUE": 3600
            }
            ]
        },
        '\n'.join(['Friday: 6 PM - 1 AM', 'Saturday: Closed'])
    ),
    (
        {
            "friDay": [{    # CamelCase
                "typE": "open",
                "valuE": 64800
            }],
            "Saturday": [{  # title-case
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

INVALID_OPENING_TIMES = [
    (
        {
            "friday": [
                {
                    "type": "open",
                    "value": 64800
                }, {
                    "type": "close",
                    "value": 64800
                }
            ]
        },
        # Two different events can not be on the same time.
    ),
    (
        {
            "friday": [
                {
                    "type": "open",
                    "value": 64800
                }
            ],
            "Saturday": [
                {
                    "type": "open",
                    "value": 64800
                }, {
                    "type": "close",
                    "value": 64800
                }
            ]
        },
        # Previous day has no closing times.
    ),
    (
        {
            "friday": [
                {
                    "type": "open",
                    "value": 64800
                }, {
                    "type": "close",
                    "value": 64800
                }
            ],
            "Saturday": [
                {
                    "type": "close",
                    "value": 64800
                }
            ]
        },
        # Closing time on Saturday has no opening time.
    )
]

OPENING_HOURS_WITH_NO_CLOSING_TIME = [
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
    )
]
