from .request import Request
from .response import Response


class RequestFilter:
    def filter(self, request: Request):
        raise NotImplementedError


class ResponseFilter:
    def filter(self, request: Request, response: Response):
        raise NotImplementedError
