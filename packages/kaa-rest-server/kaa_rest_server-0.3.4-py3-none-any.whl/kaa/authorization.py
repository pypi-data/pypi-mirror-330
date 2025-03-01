from .request import Request
from .response import Response


class Authorization:

    def authorize(self, request:Request) -> bool:
        raise NotImplementedError

    def forbidden(self, request:Request):
        return Response().forbidden(request)
