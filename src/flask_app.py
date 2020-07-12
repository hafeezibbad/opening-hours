import os
import time

from flask import Flask, g, request

from src.lib.configuration.utils import load_configuration_from_yaml_file
from src.lib.flask.http_header_helper import FlaskHttpHeaderHelper
from src.lib.logging.utils import get_flask_details_for_log, setup_logging, LOGGING
from src.app.routes.opening_hours import opening_hours_api, OPENING_HOURS_API_PREFIX
from src.app.routes.status_api import status_api, STATUS_API_PREFIX


# pylint: disable=invalid-name
app = Flask(__name__)

app_config = load_configuration_from_yaml_file(os.environ['APP_CONFIG_FILE'])
# Register blueprints
app.register_blueprint(status_api, url_prefix=STATUS_API_PREFIX)
app.register_blueprint(opening_hours_api, url_prefix=OPENING_HOURS_API_PREFIX)


@app.before_request
def before_request():       # pylint: disable=inconsistent-return-statements
    g.start_time = time.time()
    setup_logging()
    LOGGING.handlers = []
    LOGGING.propagate = False

    flask_details = get_flask_details_for_log()
    http_helper = FlaskHttpHeaderHelper()
    g.request_id = http_helper.get_request_id(request)
    request_id_details = {'request_id': g.request_id}
    initial_values = {**flask_details, **request_id_details}
    LOGGING.new(**initial_values)


@app.after_request
def after_request(response):
    LOGGING.info('REQUEST_EXECUTION_TIME', execution_time=time.time() - g.start_time)
    response.headers['X-REQUEST-ID'] = g.request_id

    return response
