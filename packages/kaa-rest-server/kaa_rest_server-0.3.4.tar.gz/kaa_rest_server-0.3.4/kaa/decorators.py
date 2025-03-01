import re

from .authorization import Authorization
from .exceptions import InvalidParamError
from .request import Request


def AUTH(auth: Authorization):
    def decorator_path(func):
        def wrapper(self, **kwargs):
            if auth.authorize(self.request):
                return func(self, **kwargs)
            return auth.forbidden(self.request)

        return wrapper

    return decorator_path


def GET(func):
    def wrapper(self, **kwargs):
        if self.request.method == "GET":
            return func(self, **kwargs)

    return wrapper


def POST(func):
    def wrapper(self, **kwargs):
        if self.request.method == "POST":
            return func(self, **kwargs)

    return wrapper


def PUT(func):
    def wrapper(self, **kwargs):
        if self.request.method == "PUT":
            return func(self, **kwargs)

    return wrapper


def PATCH(func):
    def wrapper(self, **kwargs):
        if self.request.method == "PATCH":
            return func(self, **kwargs)

    return wrapper


def DELETE(func):
    def wrapper(self, **kwargs):
        if self.request.method == "DELETE":
            return func(self, **kwargs)

    return wrapper


def PATH(uri, query_params: dict = {}, **kwargs):
    def decorator_path(func):
        def wrapper(self):
            request_path = self.request.path.strip("/")
            defined_path = uri.strip("/")

            q_params = QueryParams(self.request)
            if request_path == defined_path:
                params = q_params.get_params(query_params)
                return func(self, **params)

            split_request_path = request_path.split("/")
            split_defined_path = defined_path.split("/")

            if len(split_request_path) != len(split_defined_path):
                return

            regexp = r"^\{([a-z_][a-zA-Z0-9_]+)(:[^}]+){0,1}\}$"
            arguments = {}
            for d_path, r_path in zip(split_defined_path, split_request_path):
                if d_path == r_path:
                    continue
                m = re.search(regexp, d_path)
                if m is None:
                    return
                if m.group(2):
                    pattern = re.compile(m.group(2)[1:])
                    n = re.search(pattern, r_path)
                    if n is None:
                        return
                arguments[m.group(1)] = r_path
            arguments.update(q_params.get_params(query_params))
            return func(self, **arguments)

        return wrapper

    return decorator_path


class QueryParams:
    def __init__(self, request: Request):
        self.request = request

    def get_params(self, defined_params: dict = {}):
        params = {}
        for k in defined_params:
            params[k] = self.__get_item(k, defined_params[k])
        return params

    def __get_item(self, defined_key, defined_value):
        q_value = self.request.get_query_param(defined_key)
        if q_value:
            if "type" not in defined_value:
                return q_value
            if defined_value["type"] == "int":
                func = self.__to_int
            elif defined_value["type"] == "float":
                func = self.__to_float
            else:
                return q_value
            return self.__get_number(defined_key, q_value, func)

        if "required" in defined_value and defined_value["required"]:
            raise InvalidParamError(f"Param {defined_key} is required")

        if "default" in defined_value:
            return defined_value["default"]

    def __to_int(self, value):
        return int(value)

    def __to_float(self, value):
        return float(value)

    def __get_number(self, param, value, func):
        try:
            return func(value)
        except ValueError as error:
            raise InvalidParamError(
                f"Param {param} is not a number", error) from error
