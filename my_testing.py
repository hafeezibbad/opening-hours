import os
import sys
sys.path.append(os.getcwd())
from src.app.models.opening_hours import TimeEntry, DayTimings, OpeningHours


data = {
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
}


# data = {
#     "tuesday": [
#         {
#             "type": "open",
#             "value": 33600
#         },
#         {
#             "type": "close",
#             "value": 43600
#         }
#     ],
#     "friday": [
#         {
#             "type": "open",
#             "value": 68000
#         }
#     ]
# }
# friday_time = {
#     "type": "open",
#     "value": 64800
# }
# a = TimeEntry.load(friday_time, overridden_field_names={'type': 'status'})
# print(a)
# exit(0)


def my_func(data: dict):
    opening_hours_data = dict()

    for day, opening_times in data.items():
        day_opening_times = []
        for opening_time in opening_times:
            day_opening_times.append(TimeEntry.load(opening_time, overridden_field_names={'type': 'status'}))
        day_timings = DayTimings.load({'weekday': day, 'timings': day_opening_times})
        opening_hours_data[day] = day_timings
    return OpeningHours(**opening_hours_data)

oh = my_func(data)
print(oh.dict())
print([each for each in oh.friday])
# print(oh.saturday)
# print(oh.sunday)
