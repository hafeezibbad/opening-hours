from typing import Optional, Any


class HealthCheckService:

    def __init__(self, service: Optional[Any] = None):
        self.service = service

    def check_all(self) -> bool:
        service_status = True

        return service_status
