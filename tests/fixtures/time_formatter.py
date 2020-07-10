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
