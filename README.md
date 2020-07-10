# Opening Hours 


## Requirements
* ``python3.6`` or higher

## Known issues
* This project uses python builtin [typing](https://docs.python.org/3/library/typing.html) module, which is not
 supported for ``python3.5`` or lower. Therefore, please use ``python3.6`` or higher for running this project.  


* We currently do not handle the case where Sunday's last opening time does not have a closing time. We can not say
 with sure confidence if a closing time will be provided in next week's Monday timing. Also, if Monday has a closing
  time as first event, we take it as is (assuming that this came from last week's Sunday)


## Corner cases 
### Case 1:
If some day has an opening time, but there is not time in next day. 

#### Example:
Friday has an opening time, there is not time for next day Saturday. Therefore, essentially Friday has no closing time. 
```json
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
}
```

Exception to this is Sunday because if Sunday has an opening time and then no time afterwards, we assume that there
 will be a (closing) time in the next week Monday (as first entry).
 
### Case 2:
#### Example:
```json
{
    "friday": [
        {
            "type": "open",
            "value": 64800
        }
    ],
    "SATURDAY": [
        {
            "type": "close",
            "value": 3600
        }
    ]
}
```
In this case, Saturday will be marked as ``Closed``, instead of having any open times, for example Saturday 12AM-1AM
 
## Issues
* This works fine one one-week case, but we cannot use this to have timings for multiple weeks. There is not date
 object differentiating the days of the week.  
* When validation error is raised for `type` field to contain some value other than open|close, the pointer is
 `status`. We can change it by changing the variable name to type, but ``type`` is reserved keyword which is not
  encourage to be used as variable name
* If request payload contains duplicate data, for example, 2 Fridays etc.
* If any other key in addition to ``type``, and ``value`` is provided in Timing event, it is ignored

## Glossary
* What is timing event? its the open/close event


## Developer notes
* In timing event, ``{"type": "open", "value": 64800}``, the keys ``type`` and ``value`` are made case-insensitive by
 choice. If this behavior needs to be removed, please comment out this line from opening_hours_data_parser.py file. 
### Request IDs

### JSON logging
