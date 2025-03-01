import importlib
import sys

import kaa
from .kaa_definition import KaaDefinition

from .enums import Status
from .exceptions import KaaError, ResourceNotFoundError
from .filters import RequestFilter, ResponseFilter
from .openapi import OpenApi
from .request import Request
from .resources import Resources
from .response import Response


class Kaa:
    def __init__(self):
        self.resources = {}
        self.request_filters = {}
        self.response_filters = {}
        self.start_response = None
        self.openapi = None
        self.definitions = KaaDefinition()

    def register_resources(self, module: str, class_name: str):
        self.__register(self.resources, module, class_name)

    def register_filter_request(self, module: str, class_name):
        self.__register(self.request_filters, module, class_name)

    def register_filter_response(self, module: str, class_name):
        self.__register(self.response_filters, module, class_name)

    def __register(self, element, module, class_name):
        if module not in element:
            element[module] = []
        element[module].append(class_name)

    def serve(self, env, start_response):
        self.start_response = start_response
        request = Request(env)

        try:
            if request.method == "OPTIONS":
                return self.__act_method_options(request)

            if request.path in ("/openapi", "/openapi.yaml"):
                return self.__get_openapi(request)

            if request.path == "/openapi.json":
                return self.__get_openapi(request, "json")

            self.__request_filters(request)
            for module_name, class_names in self.resources.items():
                for class_name in class_names:
                    response: Response | None = self.__run_resource(
                        request, module_name, class_name
                    )
                    if response:
                        self.__response_filters(request, response)
                        return self.__print_response(response)
            raise ResourceNotFoundError()
        except KaaError as e:
            return self.__print_response(e.response())
        except Exception:
            return self.__print_response(
                Response().server_error(request, sys.exc_info())
            )

    def __get_openapi(self, request: Request, response_format="yaml"):
        if self.openapi is None:
            self.openapi = OpenApi().generate(self)
        response = Response()
        if (
            request.get_header("ACCEPT") == "application/json"
            or response_format == "json"
        ):
            response.json(self.openapi)
        else:
            try:
                import yaml

                response.yaml(self.openapi)
            except ImportError:
                response.json(self.openapi)
        return self.__print_response(response)

    def __act_method_options(self, request: Request):
        if self.definitions.cors_enabled():
            response = Response(Status.ACCEPTED)
            self.__response_filters(request, response)
        else:
            response = Response(Status.METHOD_NOT_ALLOWED)
        return self.__print_response(response.body(""))

    def __request_filters(self, request: Request):
        def func(instance: RequestFilter):
            method_ = getattr(instance, "filter")
            method_(instance, request)

        self.__call_filters(self.request_filters, func)

    def __response_filters(self, request: Request, response: Response):
        def func(instance: ResponseFilter):
            method_ = getattr(instance, "filter")
            method_(instance, request, response)

        self.__call_filters(self.response_filters, func)

    def __call_filters(self, filters, func):
        for module_name in filters:
            for class_name in filters[module_name]:
                func(self.__get_class(module_name, class_name))

    def __run_resource(
        self, request: Request, module_name, class_name
    ) -> Response | None:
        class_ = self.__get_class(module_name, class_name)
        instance: Resources = class_(request)
        for method_name in dir(class_):
            count = 1 + len(class_name) + 2
            if method_name[:2] == "__" or method_name[:count] == f"_{class_name}__":
                continue
            method_ = getattr(class_, method_name)
            result = method_(instance)
            if result:
                return result
        return None

    def __get_class(self, module_name, class_name):
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    def __print_response(self, response: Response):
        headers = [(k, response.headers[k]) for k in response.headers]
        headers.append(("Server", f"{kaa.NAME}/{kaa.VERSION}"))
        self.start_response(response.get_status_code(), headers)
        if response.response_body is None:
            return []
        return [response.response_body.encode("utf8")]
