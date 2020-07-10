from typing import Optional, Dict, Any

from pydantic import BaseModel

from src.app.time_formatter import TimeFormatter


class Model(BaseModel):
    @classmethod
    def load(cls, data: dict, overridden_field_names: Optional[Dict[str, str]] = None, **kwargs):
        init = {}
        for k, v in data.items():
            if overridden_field_names:
                k = overridden_field_names.get(k, k)
            if k in cls.schema()["properties"]:
                init[k] = v

        if init:
            return cls(**init, **kwargs)  # type: ignore

        raise ValueError(init)

