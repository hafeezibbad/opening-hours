DAY_TIMESTAMP_TO_HUMAN_READABLE = [
    (0, "12 AM"),
    (1, "12:00:01 AM"),
    (86399, "11:59:59 PM"),
    (43200, "12 PM"),
    (43211, "12:00:11 PM"),
    (43271, "12:01:11 PM"),
    (64800, "6 PM"),
    (36000, "10 AM")
]

UNIX_TIMESTAMP_TO_HUMAN_READABLE = [
    (1594425600.0, "12 AM"),
    (1594425601.0, "12:00:01 AM"),
    (1594511999.0, "11:59:59 PM"),
    (1594468800.0, "12 PM"),
    (1594468811.0, "12:00:11 PM"),
    (1594468871.0, "12:01:11 PM"),
    (1594490400.0, "6 PM"),
    (1594461600.0, "10 AM")
]


FORMATTED_TIME_RANGES = [
    ("5 AM", "8 AM", "5 AM - 8 AM"),
    ("5 AM", "", "5 AM - ")
]


FORMATTED_TIMES_FOR_DAY = [
    # Day names are case-insensitive example: Lower case
    ({'friday': ['6 pm - 1 am'], 'saturday': []}, "\n".join(["Friday: 6 PM - 1 AM", "Saturday: Closed"])),
    # Day names are case-insensitive example: Upper case
    ({'FRIDAY': ['6 PM - 1 AM'], 'SATURDAY': []}, "\n".join(["Friday: 6 PM - 1 AM", "Saturday: Closed"])),
    # Day names are case-insensitive example: Camel case
    ({'FriDay': ['6 Pm - 1 Am'], 'SaturDay': []}, "\n".join(["Friday: 6 PM - 1 AM", "Saturday: Closed"])),
    # Multiple timings per day
    ({'friday': ['6 am - 8 am', '6pm - 9pm']}, "Friday: 6 AM - 8 AM, 6PM - 9PM")
]
