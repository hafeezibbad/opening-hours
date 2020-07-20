import os
import sys

# PROJECT_ROOT_DIR variable is set in Makefile
from typing import Optional

sys.path.append(os.environ['PROJECT_ROOT_DIR'])

# pylint: disable=wrong-import-position
from src.flask_app import app  # noqa: E402
from src.lib.configuration.app_configuration import AppConfiguration  # noqa: E402
from src.lib.configuration.utils import load_configuration_from_yaml_file  # noqa: E402


# pylint: disable=invalid-name
app_config: Optional[AppConfiguration] = load_configuration_from_yaml_file(os.environ['APP_CONFIG_FILE'])

if app_config is not None:
    app.run(port=app_config.ServerPort, debug=app_config.Debug)
else:
    raise RuntimeError('Cannot load configuration')
