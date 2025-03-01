from .authorization import Authorization  # noqa
from .decorators import AUTH, GET, PATH, POST, PATCH, PUT, DELETE  # noqa
from .enums import ContentType, Status  # noqa
from .exceptions import (
    KaaError,
    NotFoundError,  # noqa
    ResourceNotFoundError,  # noqa
    BadRequestError,  # noqa
    UnathorizedError,  # noqa
    ForbiddenError,  # noqa
    MethodNotAllowedError,  # noqa
    InvalidParamError,  # noqa
)
from .filters import RequestFilter, ResponseFilter  # noqa
from .kaa import Kaa  # noqa
from .request import Request, RequestData  # noqa
from .resources import Resources  # noqa
from .response import Response  # noqa

NAME = "KAA"
VERSION = "0.3.4"


class KaaServer:
    def __init__(self) -> None:
        self.kaa = Kaa()
        self.register_resources()
        self.register_filters()

    def register_resources(self):
        pass

    def register_filters(self):
        pass

    def serve(self, env, start_response):
        if self.kaa is None:
            raise KaaError("Kaa is not defined")
        return self.kaa.serve(env, start_response)

    def generate_openapi(self):
        pass


class StartKaaError(Exception):
    def __init__(self, message: str):
        self.message = message
