from typing import Optional

from pydantic import conint, constr, Extra  # pylint: disable=no-name-in-module
from typing_extensions import Literal

from src.app.models.common import Model
from src.lib.configuration.validate import URL_REGEX


class AppConfiguration(Model):
    Stage: Literal["dev", "test"]
    EndpointBaseUrl: constr(regex=URL_REGEX)
    ServerPort: conint(ge=1024, le=65535)
    Debug: bool = False

    class Config:
        extra = Extra.allow     # allow extra fields (not specific in schema) in configuration object.
