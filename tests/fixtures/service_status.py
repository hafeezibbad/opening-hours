from src.app.models.status import Status

SERVICE_DOWN_STATUS = Status(message="Service is down", status="down", statusCode=503)
SERVICE_UP_STATUS = Status(message="Service is up", status="ok", statusCode=200)
