# Opening Hours 
In this project, we have developed an API which accepts JSON-formatted opening hours of a restaurant in request
 payload, and returns the opening hours in human readable format.
This API is developed using [Python](https://www.python.org/) programming language and [Flask](https://flask.palletsprojects.com/en/1.1.x/) web development framework.  

## Table of contents
* [Set up and run project locally](#set-up-and-run-project-locally)
* [API Reference](#api-reference)
* [Thoughts on JSON data](#thoughts-on-input-json)
* [Edge cases](#edge-cases)
* [Known issues](#known-issues)
* [Improvement ideas](#improvements-ideas)
* [Developer notes](#developer-notes)

## Set up and run project locally
Please follow the following instructions to set up and run this project locally. 

---
**NOTE**

The project has been developed and tested on a machine running Ubuntu 18.04 LTS operating system. The following
 instructions have been tested to run on similar operating system. 
If you are using a different operating system, please use corresponding appropriate commands for your
 system.  

---

* Make sure that you have ``Python3`` installed on your machine. If you do not have a Python3 installation on your
 machine, please follow [these instructions](https://realpython.com/installing-python/). 
 
```bash
$ python3 --version   
Python 3.X.X

```

* Set up python virtual environment for running the project 
This project uses python [venv](https://docs.python.org/3/library/venv.html) module to setup virtual
 environment. 
You can use other alternatives, such as, [pipenv](https://github.com/pypa/pipenv), 
 [virtualenv](https://github.com/pypa/virtualenv) for this purpose as well. 
 
```bash
$ make python-venv
```
You can modify the name of default virtual environment (default `venv`) by modifying ``VIRTUAL_ENV
`` variable in [Makefile](https://github.com/hafeezibbad/opening-hours/blob/master/Makefile#L2) 
If you are using some other method, instead of ``make python-venv`` target, for setting up virtual environment
, please install project dependencies by running 
 
```bash
$ pip install -r requirements-dev.txt
``` 

* Run app on your local machine using following command.
```bash
$ make app-offline

 * Serving Flask app "src.app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:3500/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 123-739-668
```
Now your server must be up and ready for usage. 
Please note that 
* This target uses [dev-configuration](https://github.com/hafeezibbad/opening-hours/blob/master/configs/app/dev/config.yml) by default. 
In case you want to run some other configuration for running the application, please modify ``STAGE`` variable in
 [Makefile](https://github.com/hafeezibbad/opening-hours/blob/master/Makefile), or run ``make app-offline`` target as, 
 
```bash
$ STAGE="test" make app-offline
```

* Once the server is up and running, you can run the end-to-end (e2e) tests against this deployment as
```bash
$ make install-and-e2e-test
```
By default the end-to-end tests use the deployment environment (STAGE) specified in [Makefile](https://github.com
/hafeezibbad/opening-hours/blob/master/Makefile#L1), but you can run the tests against any other environment as ``STAGE="test" make install-and-e2e-test``.
If you have modified ``ServerPort`` and/or ``EndpointBaseUrl`` settings in configuration file, or you want to run e2e
 tests against another deployment, please run e2e tests as ``ENDPOINT_BASE_URL='<base_url>' make e2e-test``
 
---

**Note**

For the reset of this document, _event_, _timing_event_, _timing_entry_, or simply _timing_ refer to an entry with open
/close time information, for example, ``{"type": "open", "value": 3600}``.

---

## API Reference

---

**NOTE**

Current implementation uses ``/api/v1`` prefix for all API endpoints. 
This can be changed/removed by modifying the ``OPENING_HOURS_API_PREFIX`` variable in 
[src/app/routes/opening-hours.py](https://github.com/hafeezibbad/opening-hours/blob/master/src/app/routes/opening_hours.py#L12) file. 

----
#### [POST] /api/v1/opening-hours

This endpoint accepts a valid JSON object with information about opening hours of a restaurant, and it returns a
 formatted string with human-readable 12-hour formatted opening times of the restaurant. 
For example, 
  
```bash
curl --location --request POST 'http://localhost:3500/api/v1/opening-hours' \
--header 'Content-Type: application/json' \
--data-raw '{
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
        }'
```
returns
```text
Monday: Closed
Tuesday: 10 AM - 6 PM
Wednesday: Closed
Thursday: 10 AM - 6 PM
Friday: 10 AM - 1 AM
Saturday: 10 AM - 1 AM
Sunday: 12 PM - 9 PM
```

More example with request payload and expected response are given in [tests/fixtures/opening_hours.py](https://github.com/hafeezibbad/opening-hours/blob/master/tests/fixtures/opening_hours_data.py#L1-L251)
Some edge cases for `/api/v1/opening-hours` endpoint are discussed in [Edge cases](#edge-cases) section. 

##### [GET] /api/v1/status
This API also offers a health check endpoint to poll for whether or not the service is available. 
The health check endpoint can be queried as 
```bash
curl --location --request GET 'http://localhost:3500/api/status'
```

```json
{
    "message": "Service is up",
    "status": "ok"
}
```
## Thoughts on input JSON
The current structure of input data works fine for most cases, but there are some limitations, such as, 
* Current structure does not provide a simple method to handle restaurant events which are open 24/7. If no time is
 provided for some day, it is ignored or marked as _closed_ depending on the input data.  
* Current structure supports events of one week (_Monday - Sunday_) at a time, and we can not relate events from
 _Sunday_ to following _Monday_ ([Edge case 5](#case-5)).  
* Currently, we can not handle the cases where a opening time (within a day) for a restaurant is lower than closing
 time (within a day) on following day. For example, if a restaurant opens at 10 AM on Saturday, and next closing time
  is 10 PM on Sunday. The output will be as follows, which does not accurately describe actual open times.  
```text
Saturday: 10 AM - 10 PM 
Sunday: Closed
```
* Current representation for an open or close event, for example ``[{"type": "open", "value": 3600}, {"type": "close"
, "value": 7200}]`` is not very intuitive. 

In the light of above issues, some improvements/modifications can be:
* Instead of using object for storing information about open and close events separately, we can use descriptive keys
 for timing events, as shown in following example:  
 <table>
<tr>
<th>Current</th>
<th>Alternative #1</th>
<th>Alternative #2</th>
</tr>
<tr>
<td><pre>
{
    "monday": [
        {
            "type": "open",
            "value": 32400
        },
        {
            "type": "close",
            "value": 61200
        }
    ]
}</pre></td>
<td><pre>{
    "monday": [
        {
            "opening_time": 32400,
            "closing_time": 61200
        }
    ]
}</pre></td>
<td><pre>{
    "monday": [
        {
            "open": 32400,
            "close": 61200
        }
    ]
}</pre></td>
</tr>
</table>

These alternatives are developer-friendly and intuitive, and will simplify parsing and validation logic. 
To handle missing closing or opening time, we can use additional (boolean) field(s) such as ``opens_previous_day
`` and ``closes_next_day`` to indicate that the restaurant's opening time and closing times are from previous and
 nextday, respectively. 
These additional fields will simplify the logic to handle events when opening and closing
  times span over days. 
 
* JSON data can be further restructured to provide information about events of a day using descriptive keys, that are
, `day`, `events`. An example is shown as follows.  

*  JSON structure can be further improved, such that instead of having days of weeks as keys, descriptive keys `day
`, and `events` are used, where `day` will contain weekday, and  _events_ will contain data for opening
 and closing events. This will also help in establishing common understanding of _events_ in data.

<table>
<tr>
<th>Current</th>
<th>Alternative #1</th>
<th>Alternative #2</th>
</tr>
<tr>
<td><pre>
{
    "monday": [
        {
            "type": "open",
            "value": 32400
        },
        {
            "type": "close",
            "value": 61200
        }
    ]
}</pre></td>
<td><pre>
{
    [
        "day": "monday",
        "events": [
            {
                "opening_time": 32400,
                "closing time": 61200
            }
        ]
    ]
}</pre></td>
<td><pre>
{
    [
        "day": "monday",
        "events": [
            {
                "open": 32400,
                "close": 61200
            }
        ]
    ]
}</pre></td>
</tr>
</table>

This representation will remove additional logic required to extract and process weekday information from  _keys_ in
 JSON data. 

* To compress the representation of input data, we can combine all opening and closing events of a day within
 a single object. For example,  
  
<table>
<tr>
<th>Current</th>
<th>Alternative #1</th>
<th>Alternative #2</th>
</tr>
<tr>
<td><pre>{
    "monday": [
        {
            "type": "open",
            "value": 32400
        },
        {
            "type": "close",
            "value": 56400
        },
        {
            "type": "open",
            "value": 61200
        },
        {
            "type": "close",
            "value": 68600
        }
    ]
}</pre></td>
<td><pre>{
    "monday": [
        {
            "opening_time": [32400, 61200],
            "closing_time": [56400, 68600]
        }
    ]
}</pre></td>
<td><pre>{
    "monday": [
        {
            "open": [32400, 61200],
            "close": [56400, 68600]
        }
    ]
}</pre></td>
</tr>
</table>

While this representation is compressed, this will require additional logic to create a chain of events, such as 
``{"monday": [("open", 32400), ("close", 56400), ("open", 61200), ("close", 68600)]}`` before getting restaurant opening
 and closing times. 
## Edge cases 
### Case 1:
If last event for given day is _open_, and there is no event for the following day, we raise an error that there is
 not closing event available for last _open_ event of current day.  

In the following example _Friday_ has an opening time, and there is no event for next day (Saturday).
Typically, in such cases, closing time for _Friday_ will be the first _close_ event given in next day, that
 is, _Saturday_. 
However, since we do not have any data for _Saturday_, we raise an error that _Friday_ has no closing time.  
One exception to this behavior is _Sunday_, which is discussed in [Case 4](#case-4). 
```bash
curl --location --request POST 'http://localhost:3500/api/v1/opening-hours' \
--header 'Content-Type: application/json' \
--data-raw '{
    "friday": [
        {
            "type": "open", 
            "value": 57600
        }
    ],
    "sunday": [
        {
            "type": "close", 
            "value": 12345
        },
        {
            "type": "open",
            "value": 82800
        }
    ]
}'
```

```json
{
    "errors": [
        {
            "title": "Missing closing time",
            "detail": "`Friday: 4 PM` has no closing time on following day",
            "source": {
                "pointer": "friday"
            }
        }
    ],
    "message": "Opening hours parsing failed"
}
```

More examples of this case are given in 
[tests/fixtures/opening_hours.py](https://github.com/hafeezibbad/opening-hours/blob/master/opening_hours_data.py#L352-L557)/ 
### Case 2
If a day only has closing time from previous day, it will be considered _Closed_.
In the following example, _Saturday_ will be marked as _Closed_, instead of having any open times of _Saturday 12AM - 1AM_
```bash
{
    "friday": [
        {
            "type": "open",
            "value": 64800
        }
    ],
    "saturday": [
        {
            "type": "close",
            "value": 3600
        }
    ]
}
```

```text
Friday: 6 PM - 1 AM
Saturday: Closed
```
### Case 3
This case is related to [Case 1](#case-1).
If the last event for given day is _open_, and the first event on following day is not _close_, the API returns an
 error explaining that given day's _open_ event has no closing time. 
 
In the following example, _Monday_ has an open even with no closing time. It is assumed that the first entry on
 following day _Tuesday_ will be close event for existing open event from Monday. 
However, the first event on _Tuesday_ is open, resulting in an error that _Monday_ open event has no closing time. 
```bash
curl --location --request POST 'http://localhost:3500/api/v1/opening-hours' \
--header 'Content-Type: application/json' \
--data-raw '{
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
}'
``` 

```json
{
    "errors": [
        {
            "title": "Missing closing times",
            "detail": "`Monday: 9 AM` has no closing time",
            "source": {
                "pointer": "monday"
            }
        }
    ],
    "message": "Opening hours parsing failed"
}
```

More examples for this case can be found in [tests/fixtures/opening_hours_data.py](https://github.com/hafeezibbad/opening-hours/blob/master/tests/fixtures/opening_hours_data.py#L352-L558)
### Case 4
This case is related to [case 1](#case-1) and [case-3](#case-3). 
If current day is Sunday, and the last event is _open_, instead of raising an error about no closing time, we assume
 that there will be a closing time (as first entry) in the next week Monday .
Following this decision, there are two choices for displaying human-readable opening times for _Sunday_
1. We do not mark opening time for last opening event on Sunday.  
2. We show open interval on last opening event on Sunday. 

Following example shows that current implementation follows Choice #2, however, it should be possible to use choice #1 
by commenting out [this code segment lines](https://github.com/hafeezibbad/opening-hours/blob/master/src/app/service/opening_hours.py#L47-L50).
```bash
curl --location --request POST 'http://localhost:3500/api/v1/opening-hours' \
--header 'Content-Type: application/json' \
--data-raw '{
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
}'
```

```text
Sunday: 3 PM - 5 PM, 8 PM -
```
The output following choice #1 will be ``Sunday: 3 PM - 5 PM``.

More variations of this case are given in [tests/fixtures/opening_hours.py] 

### Case #5 
If the first event of week is _close_, we ignore this event. 
In the following example, we ignore first _close_ event for Monday. 
```json
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
}
```
```text
Monday: 9 AM - 5 PM
```

More examples of this case can be found in [tests/fixtures/opening_hours_data.py](https://github.com/hafeezibbad/opening-hours/blob/master/tests/fixtures/opening_hours_data.py#L765-L850)

## Known issues
* If request payload contains duplicate data, for example, 2 Fridays etc.
* If any other key in addition to ``type``, and ``value`` is provided in Timing event, it is ignored during data
 parsing, and no validation error is raised. 
* Test classes (for example, [TestTimeFormatter](https://github.com/hafeezibbad/opening-hours/blob/master/tests/unit
/app/test_time_formatter.py)) are not subclassed this from ``unittest.TestCase`` because parametrization is not
 supported for subclasses of ``unittest.TestCase`` [reference](https://docs.pytest.org/en/latest/unittest.html#pytest  -features-in-unittest -testcase-subclasses).
* For each day when a restaurant is closed, current implementation requires ``<day>: []`` to be passed in input data.
This behavior can be changed by modifying ``monday: DayTimings = DayTimings.load({"weekday": "monday"})`` to 
``monday: DayTimings = DayTimings.load({"weekday": "monday", "timings": []})`` in [src/app/models/opening_hours.py](https://github.com/hafeezibbad/opening-hours/blob/master/src/app/models/opening_hours.py#L105-L111). 
A side effect of this would be if there is not data provided for a day, it will be marked as closed. For example,

<table>
<tr>
<th>Before</th>
<th>After</th>
</tr>
<tr>
<td><pre>
Friday: 6 PM - 1 AM
Saturday: Closed
</pre></td>
<td><pre>
Monday: Closed
Tuesday: Closed
Wednesday: Closed
Thursday: Closed
Friday: 6 PM - 1 AM
Saturday: Closed
Sunday: Closed
</pre></td>
</tr>
</table>

* Static analysis using [mypy](https://mypy.readthedocs.io/en/stable/introduction.html) has some errors. These do not
 directly affect the application functionality.   
## Improvements ideas
* Test coverage (both unit test and end-to-end) can be improved.
* Deployment using public cloud, such as [Heroku](https://www.heroku.com/), [AWS](https://aws.amazon.com/).
* Run application in a docker container. 
* Add rate limiting to the API to prevent (D)DoS attacks.
* Add caching support for the API calls. 
* Add Authentication and Authorization. [JSON web tokens](https://jwt.io/) are a good candidate.
## Developer notes
* In current implementation, ``type`` and ``value`` keys in timing events, for example, ``{"type": "open", "value
": 64800}``, are case-insensitive. If this behavior is not required, please comment out this line from [src/app
 /request_parser/opening_hours_data_parser.py#L26]. 
* Current implementation uses ``status`` variable to store information given in `type` field. This means we have to
 do additional conversion in parsing request data and creating response data. The reason for choosing variable name
  ``status`` instead of ``type`` is because ``type`` is reserved-keyword in python. 
 
### Time resolution 
* Current implementation provides human-readable opening times with resolution up to seconds, that is ``11:59:59 PM``. 
If we need to modify this resolution, it can be done by modifying 
[this code segment](https://github.com/hafeezibbad/opening-hours/blob/master/src/app/utils/time_formatter.py#L10-L15).
* In case of errors (discussed in [Edge cases](#edge-cases)), we provide human readable data in error message instead
 of given value. This can be changed to provide ``value`` by modifying 
 ``last_time=TimeFormatter.get_human_readable_time_from_timestamp(error_data.get('last_time', 0)),`` to 
 ``last_time=error_data.get('last_time', 0),`` 
 [here](https://github.com/hafeezibbad/opening-hours/blob/master/src/app/models/opening_hours.py#L123).
 
 
### Python requirement
The project was developed using ``python3.6``. The project uses [typing](https://docs.python.org/3/library/typing.html) 
module, which will not work with ``python3.5`` or lower.
If your system default ``python3`` is ``python3.5`` or lower, please 
* either modify the ``PYTHON_RUNTIME`` variable in [Makefile](https://github.com/hafeezibbad/opening-hours/blob/master/Makefile#L5) to use a different version of file
* or set environment variable ``PYTHON_RUNTIME`` to specific python version 
```bash
export PYTHON_RUNTIME=python3.6
```
### Choice of Flask
The choice of [flask](https://flask.palletsprojects.com/en/1.1.x/) as the framework for this project was motivated by
 the ease of development of flask. 
The modular structure of makes flask lightweight and quick to prototype.
Meanwhile, we can extend the application functionality using various modules supported to work with flask.   
 
### Code analysis
This project uses [pylint](https://pypi.org/project/pylint/) and [pycodestyle](https://pypi.org/project/pycodestyle/) 
guidelines to check code styling and formatting issues. 
After making code changes, code-styling and basic analysis checks can be performed as 

```bash
$ make analyze-code
```

The default configuration for pylint checks can be overridden by modifying 
[pylint-configuration file](https://github.com/hafeezibbad/music_app/blob/master/configs/pylint/pylint.cfg)

You can also run static analysis using [mypy](https://mypy.readthedocs.io/en/stable/introduction.html)
```bash
$ make static-analysis
```
### Running unit tests
Unit tests are included in [tests/unit](https://github.com/hafeezibbad/opening-hours/tree/master/tests/unit) directory.
Unit tests can be run using ``make test`` target.
This target assumes that ``make python-venv`` has been run earlier, and python virtual environment already exists with
 all dependencies installed. 
In case python virtual environment does not exist, run ``make install-and-test`` to set up virtual environment
 and then run unit tests.  

You can specify minimum unit test coverage for new changes by modifying ``MIN_UNIT_TEST_COVERAGE`` 
[here](https://github.com/hafeezibbad/opening-hours/blob/master/Makefile#L8). 

### Request IDs
All responses from opening-hours API return a request ID in X-REQUEST-ID response header 
This request ID uniquely identifies a single request in logs, and is helpful for debugging purposes. 
Clients can pass request ID in X-REQUEST-ID header to any request and assuming it is valid ([pattern
](https://github.com/hafeezibbad/opening-hours/blob/master/src/lib/request_id/validator.py#L5), it
 will be used throughout the request, and returned in response as well. 
In case request ID is invalid or missing from request, it will be auto-generated and returned on each response.
### Logging
Current implementation logs all exceptions in developer-friendly JSON format. 
This also helps in log analysis as log processing systems, for example, [Splunk](https://www.splunk.com), may offer
 support for automatic parsing and processing of logs in JSON format.

Each log entry contains ``user-agent``, ``timestamp`` of event, and ``request_id`` to map the client API request to
 logs. In addition to these fields, 
* For all incoming requests, we log ``request_data``
```json
{
	"user_agent": "PostmanRuntime/7.26.1",
	"request_id": "0000-894b756bdd8a45cb9c07e07ac2ce9742",
	"message": "Opening hour parsing started",
	"request_method": "POST",
	"request_path": "/api/v1/opening-hours",
	"request_data": {
		"sunday": [{
			"type": "open",
			"value": 54000
		}, {
			"type": "close",
			"value": 61200
		}, {
			"type": "open",
			"value": "72000"
		}]
	},
	"request_args": null,
	"event": "HTTP_REQUEST",
	"timestamp": "2020-07-12T10:13:49.313487Z"
}
```
* For failed requests, we log all exceptions, validation errors, and data parsing errors with full stack trace 
```json
{
	"user_agent": "PostmanRuntime/7.26.1",
	"request_id": "0000-14f158860045498bb6907595c3adaa75",
	"message": "Invalid JSON format provided in request body",
	"verbose_message": null,
	"request_method": "post",
	"request_path": "/api/v1/opening-hours",
	"response_status_code": 400,
	"exception_details": {
		"exception_class": "AppSimpleError",
		"exception_message": "Invalid JSON format provided in request body",
		"exception_traceback_details": {
			"filename": "/path/to/folder/opening-hours/src/app/routes/opening_hours.py",
			"lineno": 19,
			"name": "parse_opening_hours",
			"type": "AppSimpleError"
		},
		"exception_traceback": "Traceback (most recent call last):\n  File \"/path/to/folder/opening-hours/src/app/manager.py\", line 43, in parse_request_data_as_json\n    return json.loads(request_data)\n  File \"/usr/lib/python3.6/json/__init__.py\", line 354, in loads\n    return _default_decoder.decode(s)\n  File \"/usr/lib/python3.6/json/decoder.py\", line 342, in decode\n    raise JSONDecodeError(\"Extra data\", s, end)\njson.decoder.JSONDecodeError: Extra data: line 1 column 9 (char 8)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/path/to/folder/opening-hours/src/app/routes/opening_hours.py\", line 19, in parse_opening_hours\n    request_data: dict = manager.parse_request_data_as_json(request.get_data())\n  File \"/path/to/folder/opening-hours/src/app/manager.py\", line 47, in parse_request_data_as_json\n    message='Invalid JSON format provided in request body'\nsrc.app.errors.AppSimpleError\n"
	},
	"event": "OPENING HOURS APP_ERROR",
	"timestamp": "2020-07-12T10:25:30.470386Z"
}
```
* For successful requests, we log ``response_data``, ``header``, and other details
```json
{
	"user_agent": "PostmanRuntime/7.26.1",
	"request_id": "0000-8958bbbca207493ca375ab1864b52e82",
	"message": "Opening hours parsing successful",
	"request_method": "POST",
	"request_path": "/api/v1/opening-hours",
	"response_status_code": 200,
	"response_data": "Monday: 9 AM - 5 PM",
	"response_extra_headers": null,
	"event": "HTTP_RESPONSE",
	"timestamp": "2020-07-12T12:05:19.017607Z"
}
```
and ``request_execution_time``
```json
{
	"user_agent": "PostmanRuntime/7.26.1",
	"request_id": "0000-69b8a66b71574f40aaa56e04bfadefb7",
	"execution_time": 0.0005064010620117188,
	"event": "REQUEST_EXECUTION_TIME",
	"timestamp": "2020-07-12T11:05:16.430990Z"
}
```
### Health check
Currently, the health check service checks if application is up and running, server is accessible, and application
 configuration is loaded successfully. 
As application evolves, health check processes can be extended to verify all dependencies for running the application.   
