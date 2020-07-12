# Opening Hours 
In this project, we have developed an API which accepts JSON-formatted opening hours of a restaurant in request
 payload, and returns the opening hours in human readable format.
This API is developed using [Python](https://www.python.org/) programming language and [Flask](https://flask.palletsprojects.com/en/1.1.x/) web development framework.  

## Requirements
* ``python3.6`` or higher

## Set up and run project locally
Please follow the following instructions to set up and run this project locally. 

---
**NOTE**

The project has been developed and tested on a machine running Ubuntu 18.04 LTS operating system. The following
 instructions have been tested to run on similar operating systems. 
If you are using a different operating system, please use corresponding appropriate commands for your operating
 system.  

---

* Make sure that you have ``Python3`` installed on your machine.
 
```bash
$ python3 --version   
Python 3.X.X

```
If you do not have a Python3 installation on your machine, please follow the instructions given 
[here](https://realpython.com/installing-python/). 
The project was developed using ``python3.6``. The project uses [typing](https://docs.python.org/3/library/typing.html) 
module, which will not work with python versions lower than ``python3.6``.
If your system default ``python3`` is ``python3.5`` or lower, please 
* either modify the ``PYTHON_RUNTIME`` variable in [Makefile](https://github.com/hafeezibbad/music_app/blob/master/Makefile) to use a different version of file
```text
PTYHON_RUNTIME ?= python3.6
``` 

* or set environment variable ``PYTHON_RUNTIME`` to specific python version 
    
```bash
export PYTHON_RUNTIME=python3.6
```   


 
* Set up python virtual environment for setting up the project 
This project uses python [venv](https://docs.python.org/3/library/venv.html) module to setup virtual
 environment. You can use other alternatives, such as, [pipenv](https://github.com/pypa/pipenv), 
 [virtualenv](https://github.com/pypa/virtualenv) for this purpose as well. 
 
```bash
$ make python-venv
```
You can modify the name of default virtual environment (set up by ``make`` target) by modifying ``VIRTUAL_ENV
`` variable in [Makefile](https://github.com/hafeezibbad/music_app/blob/master/Makefile) 
In case you are using some other method instead of ``make python-venv`` target for setting up virtual environment
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
* This target uses [dev-configuration]() by default. In case you want to run some other configuration
 for running the application, please modify ``STAGE`` variable in [Makefile](), or run this target as. 
 
```bash
$ STAGE="test" make app-offline
```

* Once the server is up and running, you can run the end-to-end tests against this deployment as
```bash
$ make install-and-e2e-test
```
By default the end-to-end tests use the deployment environment (STAGE) specified in [Makefile](), but you can run the
 tests against any other environment as ``STAGE="test" make install-and-e2e-test``
If you have modified ``ServerPort`` and/or ``EndpointBaseUrl`` settings in configuration file, or you want to run
 tests against another deployment of this app, please run e2e tests as ``ENDPOINT_BASE_URL='<base_url>' make e2e-test``
 
## API Reference

---

**NOTE**

We use ``/api/v1`` prefix for all API endpoints. This can be changed/removed by modifying the ``OPENING_HOURS_API_PREFIX
`` variable in [src/app/routes/opening-hours.py]() file. 

----

##### [POST] /api/v1/opening-hours

This endpoint accepts a valid JSON object with information about opening hours of a restaurant, and it returns a
 formatted string with human-readable 12-hour formatted opening times of the restaurant. For example, following API
  call will return
  
```bash
curl --location --request POST 'http://localhost:3500/api/v1/opening-hours' \
--header 'Content-Type: application/json' \
--data-raw '{
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

More example with request payload and expected response are given in [tests/fixtures/opening_hours.py]
 

### [GET] /api/v1/status
Opening hours API offers a health check endpoint to poll for whether or not the service is available. 
The health check endpoint can be queried as 
```bash
curl --location --request GET 'http://localhost:3500/api/status' \
--header 'Content-Type: application/json' \
--data-raw '{
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
}'
```

```json
{
    "message": "Service is up",
    "status": "ok"
}
```
 
---

**Note**

In this project, _event_, _timing_event_, _timing_entry_, or simply _timing_ refer to an entry with open/close time
 information, for example, ``{"type": "open", "value": 3600}``.
  
---

## Known issues
* This project uses python builtin [typing](https://docs.python.org/3/library/typing.html) module, which is not
 supported for ``python3.5`` or lower. Therefore, please use ``python3.6`` or higher for running this project.  
* Current implementation handles following edge cases in particular manner due to implementation choice. This can be
 modified based on requirements and functionality of clients using this API. 
 We discuss some of these edge cases as. 

### Edge cases 
### Case 1:
If last event for given day is _open_, and there is no event for the following day, we raise an error that there is
 not closing event available for last _open_ event of current day.  
#### Example:
In the following example, Friday has an opening time, and there is no event for next day (Saturday).
Typically, in such cases, closing time for _Friday_ will be the first _close_ event given in next day, which would
 naturally be _Saturday_. 
However, since we do not have any data for _Saturday_, we raise an error that _Friday_ has
  no closing time. 
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
            "type": "close", "value": 12345
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

One exception to this behavior is _Sunday_, which is discussed in Case 3. 

More variations of this case are given in [tests/fixtures/opening_hours.py] 
### Case #2:
If a day only has closing time from previous day, it will be considered _Closed_
#### Example:
In the following example, Saturday will be marked as _Closed_, instead of having any open times of Saturday 12AM-1AM
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
More variations of this case are given in [tests/fixtures/opening_hours.py] 

### Case 3:
This case is related to Case 1.
If the last event for given day is _open_, and the first event on following day is not _close_, the API returns an
 error explaining that given day's _open_ event has no closing time. 
 
In the following example, 
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
            "title": "Missing closing time",
            "detail": "`Tuesday: 9 AM` has no closing time",
            "source": {
                "pointer": "tuesday"
            }
        }
    ],
    "message": "Opening hours parsing failed"
}
```


### Case 4:
This case is related to case 1 and 3. 
If given day is Sunday, and the last event in _open_, instead of raising an error about no closing time, we assume
 that there will be a (closing) time in the next week Monday (as first entry).
Following this decision, there are two choices for specifying the opening times for _Sunday_
1. We do not mark opening time for last opening event on Sunday.  
2. We show open interval on last opening event on Sunday. 

Following example shows that current implementation follows Choice #2, however, it should be possible to use choice #1 
by commenting out these lines [src/app/service/opening_hours.py#L56-57]
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
The output for choice #1 will be ``Sunday: 3 PM - 5 PM``.

More variations of this case are given in [tests/fixtures/opening_hours.py] 

### Case #5: 
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

More examples can be found [tests/fixtures/opening_hours_data.py#L711-795]
## Issues
* This works fine one one-week case, but we cannot use this to have timings for multiple weeks. There is not date
 object differentiating the days of the week.  
* When validation error is raised for `type` field to contain some value other than open|close, the pointer is
 `status`. We can change it by changing the variable name to type, but ``type`` is reserved keyword which is not
  encourage to be used as variable name
* If request payload contains duplicate data, for example, 2 Fridays etc.
* If any other key in addition to ``type``, and ``value`` is provided in Timing event, it is ignored
* Cannot subclass this from unittest.TestCase because parametrization is not support [reference](https://docs.pytest.org/en/latest/unittest.html#pytest-features-in-unittest-testcase-subclasses)

## Improvements ideas
* Test coverage (both unit test and end-to-end) can be improved.
* Deployment using public cloud, such as [Heroku](https://www.heroku.com/), AWS(https://aws.amazon.com/)
* Dockerization of flask app. 
* Add rate limiting and caching to the API to prevent (D)DoS attacks. 
* Add Authentication and Authorization. JSON web tokens are a good candidate.

## Thoughts on Data format
The current format of data works well

## Developer notes
* In timing events, ``{"type": "open", "value": 64800}``, the keys ``type`` and ``value`` are made case-insensitive by
 choice. If this behavior is not required, please comment out this line from [src/app
 /request_parser/opening_hours_data_parser.py file#L26]. 
 
### Code analysis
#### Code analysis
This project uses [pylint](https://pypi.org/project/pylint/) and [pycodestyle](https://pypi.org/project/pycodestyle/) 
guidelines to check code styling and formatting issues. 
After making code changes, code-styling checks can be performed as 

```bash
$ make analyze-code
```

The default configuration for pylint checks can be overridden by modifying 
[pylint-configuration file](https://github.com/hafeezibbad/music_app/blob/master/configs/pylint/pylint.cfg)

### Running unit tests
Unit tests are included in [tests/unit]() directory. These tests can be run using ``make test`` target. It assumes
 that ``make python-venv`` has been done earlier, and python virtual environment already exists with all dependencies
  installed. 
In case python virtual environment does not exist, run ``make install-and-test`` to install set up virtual environment
 and then run unit tests.  

### Request IDs
All requests return a request ID in X-REQUEST-ID response header 
This request ID uniquely identifies a single request in logs, and is helpful for debugging purposes. 
Client can pass request ID in X-REQUEST-ID header to any request and assuming it’s valid (following this [pattern](), it
 will be used throughout the request, and returned in response as well. 
In case request ID is invalid or missing from request, it will be auto-generated and returned on each response.

### Logging
This project logs all exceptions in developer-friendly JSON format. This also helps in log analysis as log processing
 systems, for example, Splunk, offer support for automatic parsing and processing of logs in JSON format.

Each log entry contains ``user-agent``, ``timestamp`` of event, and ``request_id`` to map the client API request to
 logs. In addition to above, 
* For all incoming requests, we log ``request_data``;
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
* For failed requests, we log all exceptions, validation errors, and data parsing errors with full stack trace; 
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
			"filename": "/home/dev/personal/projects/opening-hours/src/app/routes/opening_hours.py",
			"lineno": 19,
			"name": "parse_opening_hours",
			"type": "AppSimpleError"
		},
		"exception_traceback": "Traceback (most recent call last):\n  File \"/home/dev/personal/projects/opening-hours/src/app/manager.py\", line 43, in parse_request_data_as_json\n    return json.loads(request_data)\n  File \"/usr/lib/python3.6/json/__init__.py\", line 354, in loads\n    return _default_decoder.decode(s)\n  File \"/usr/lib/python3.6/json/decoder.py\", line 342, in decode\n    raise JSONDecodeError(\"Extra data\", s, end)\njson.decoder.JSONDecodeError: Extra data: line 1 column 9 (char 8)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/dev/personal/projects/opening-hours/src/app/routes/opening_hours.py\", line 19, in parse_opening_hours\n    request_data: dict = manager.parse_request_data_as_json(request.get_data())\n  File \"/home/dev/personal/projects/opening-hours/src/app/manager.py\", line 47, in parse_request_data_as_json\n    message='Invalid JSON format provided in request body'\nsrc.app.errors.AppSimpleError\n"
	},
	"event": "OPENING HOURS APP_ERROR",
	"timestamp": "2020-07-12T10:25:30.470386Z"
}
```
* For successfully requests, we log and ``request execution times``;
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
Currently, the health check service checks is application is up and running, server is accessible, and application
 configuration is loaded successfully. 
As application evolves, health check processes can be extended.   
