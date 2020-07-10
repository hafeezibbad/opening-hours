from typing import Dict, List

from rest_framework import serializers

EVENT_TYPE_OPEN = 'open'
EVENT_TYPE_CLOSE = 'close'

EVENT_TYPE_CHOICES = (EVENT_TYPE_OPEN, EVENT_TYPE_CLOSE)

""" Contains formatting functions used by the services. """
import arrow


def format_time(timestamp: int) -> str:
    """
    Converts Unix timestamp to a human readable time
    in the format h:mm:ss AM/PM
               or h:mm AM/PM if the seconds are '00'
               or h AM/PM if the minutes are '00'
    """
    # Current time is in EET zone, so convert it to UTC
    current_time = arrow.Arrow.fromtimestamp(timestamp).to('UTC')
    formatted_time = current_time.format('h:mm:ss A')
    if current_time.format('ss') == '00':
        formatted_time = current_time.format('h:mm A')
        if current_time.format('mm') == '00':
            formatted_time = current_time.format('h A')

    return formatted_time


def format_time_range(opening_time: str, closing_time: str) -> str:
    """ Returns a formatted string representing an opening time and closing time pair. """
    return f'{opening_time} - {closing_time}'


def format_output(data: dict) -> str:
    """ Returns the human readable string from the formatted dict. """
    lines = []
    for day, times in data.items():
        if times:
            lines.append(f'{day.title()}: {", ".join(times)}')
        else:
            lines.append(f'{day.title()}: Closed')
    formatted_output = '\n'.join(lines)

    return formatted_output


class EventSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=EVENT_TYPE_CHOICES)
    value = serializers.IntegerField(min_value=0, max_value=86399)


class DaySerializer(serializers.Serializer):
    monday = EventSerializer(many=True)
    tuesday = EventSerializer(many=True)
    wednesday = EventSerializer(many=True)
    thursday = EventSerializer(many=True)
    friday = EventSerializer(many=True)
    saturday = EventSerializer(many=True)
    sunday = EventSerializer(many=True)

    def validate(self, data: dict) -> dict:
        """
        Check for the following cases:
            1) If there are two consecutive events of the same type --> raise error.
            2) If first and last event types of the week are the same, or
            3)     there is only one event in the whole week --> raise error.
        """
        first_event_type = None
        previous_event_type = None
        for day, events in data.items():
            for event in events:
                if event['type'] == previous_event_type:
                    raise serializers.ValidationError(f'Cannot have two consecutive "{event["type"]}" times.')
                else:
                    previous_event_type = event['type']

                if first_event_type is None:
                    first_event_type = event['type']
        if first_event_type == previous_event_type:
            raise serializers.ValidationError('You must start and end a week with events of distinct types.')

        return data

def to_human_readable_times(data: dict) -> str:
    """ Main service to parse the input then format it to human readable times"""
    parsed_times_dict = parse_input_times(data)
    human_readable_times = format_output(parsed_times_dict)

    return human_readable_times


def parse_input_times(data: dict) -> Dict[str, List[str]]:
    """
    Parses the serialized data dict and convert it to a dict of human readable data
    in the format: {day: list_of_opening_hour_ranges_per_day}
    """
    opening_time = None
    day_of_opening_time = None
    overflowing_closing_time = None
    times_dict = {}
    for day, events_of_a_day in data.items():
        times_dict[day] = []
        for event in events_of_a_day:
            if event['type'] == EVENT_TYPE_OPEN:
                opening_time = format_time(event['value'])
                day_of_opening_time = day
            else:
                closing_time = format_time(event['value'])
                if opening_time is not None:
                    times_dict[day_of_opening_time].append(format_time_range(opening_time, closing_time))
                else:
                    overflowing_closing_time = closing_time

    if overflowing_closing_time:
        times_dict[day].append(format_time_range(opening_time, overflowing_closing_time))

    return times_dict

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


def check_data(data: dict) -> dict:
    """
    Check for the following cases:
        1) If there are two consecutive events of the same type --> raise error.
        2) If first and last event types of the week are the same, or
        3)     there is only one event in the whole week --> raise error.
    """
    first_event_type = None
    previous_event_type = None
    for day, events in data.items():
        for event in events:
            if event['type'] == previous_event_type:
                raise serializers.ValidationError(f'Cannot have two consecutive "{event["type"]}" times.')
            else:
                previous_event_type = event['type']

            if first_event_type is None:
                first_event_type = event['type']
    if first_event_type == previous_event_type:
        raise serializers.ValidationError('You must start and end a week with events of distinct types.')

    return data

print(check_data(data))


# serializer = DaySerializer(data=data)
# print(serializer.is_valid())
# if serializer.is_valid():
#     response_data = to_human_readable_times(serializer.data)
#
# print(response_data)
