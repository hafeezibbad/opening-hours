from typing_extensions import Literal


from src.app.models.common import Model


class Status(Model):
    message: str
    status: str
    statusCode: Literal[200, 503]

    def get_status_data(self):
        fields: dict = self.dict()
        del fields['statusCode']

        return fields
