from typing import Optional


class ServiceError(RuntimeError):
    def __init__(self, message: Optional[str] = None):
        self.message = message
