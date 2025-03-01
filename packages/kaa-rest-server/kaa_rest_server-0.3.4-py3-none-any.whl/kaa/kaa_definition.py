import json
import os
import sys
import logging
from typing import Any
from threading import Lock


class KaaDefinitionMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class KaaDefinition(metaclass=KaaDefinitionMeta):
    DEFINITION_FILE = "kaa.json"
    DEFAULT_NAME = "Generic name"
    DEFAULT_VERSION = "v0"
    DEFAULT_ROOT_PATH = "."
    DEFAULT_DEBUG = False
    DEFAULT_ENABLE_CORS = False

    DEFAULT_POLLING_ENABLED = True
    DEFAULT_POLLING_INTERVAL = 1
    DEFAULT_POLLING_INCLUDE = []
    DEFAULT_POLLING_EXCLUDE = [
        ".git",
        ".idea",
        "__pycache__",
        "venv",
        "*.pyc",
        "*.md",
        "*.log",
        "LICENSE",
    ]

    host = "localhost"
    port = 5321

    definition_data: dict[str, Any]

    def __init__(self, definition_path=None) -> None:
        self.log = logging.getLogger()
        if not definition_path:
            definition_path = f"{os.getcwd()}/{self.DEFINITION_FILE}"
        if os.path.isfile(definition_path):
            self.definition_data = self.__get_json_definition_data(definition_path)
        else:
            self.definition_data = self.__get_default_definition()

        self.get_server()

    def __get_json_definition_data(self, definition_path):
        try:
            with open(definition_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as err:
            raise DefinitionException(f"{definition_path} is not a valid JSON") from err

    def set_host(self, host):
        self.definition_data["host"] = host

    def set_port(self, port):
        self.definition_data["port"] = port

    def get_server(self):
        if "server" in self.definition_data.keys():
            return self.definition_data["server"]
        raise DefinitionException("server is not defined")

    def get_name(self):
        return self.__get_definition("name", self.DEFAULT_NAME)

    def get_version(self):
        return self.__get_definition("version", self.DEFAULT_VERSION)

    def get_host(self):
        return self.__get_definition("host", self.host)

    def get_port(self):
        return self.__get_definition("port", self.port)

    def get_root_path(self):
        return self.__get_definition("rootPath", self.DEFAULT_ROOT_PATH)

    def is_polling_enabled(self):
        return self.__get_polling_definition("enabled", self.DEFAULT_POLLING_ENABLED)

    def get_polling_interval(self):
        return self.__get_polling_definition(
            "intervalSeconds", self.DEFAULT_POLLING_INTERVAL
        )

    def get_polling_paths(self):
        return (
            self.__get_polling_definition("include", self.DEFAULT_POLLING_INCLUDE),
            self.__get_polling_definition("exclude", self.DEFAULT_POLLING_EXCLUDE),
        )

    def is_debug(self):
        return self.__get_definition("debug", self.DEFAULT_DEBUG)

    def cors_enabled(self):
        return self.__get_definition("enableCors", self.DEFAULT_ENABLE_CORS)

    def __get_polling_definition(self, key, default_value):
        development_polling = self.__get_definition("developmentPolling", {})
        return self.__get_value(development_polling, key, default_value)

    def __get_definition(self, key, default_value):
        return self.__get_value(self.definition_data, key, default_value)

    def __get_value(self, data, key, default_value):
        return data[key] if key in data.keys() else default_value

    def __get_default_definition(self):
        try:
            import definitions # type: ignore # no requirements

            definition_data = {
                "name": self.__get_module_name(definitions, self.DEFAULT_NAME),
                "version": self.__get_module_version(definitions, self.DEFAULT_VERSION),
                "server": self.__get_module_server(definitions),
                "debug": self.__get_module_debug(definitions, self.DEFAULT_DEBUG),
                "enableCors": self.__get_module_cors(
                    definitions, self.DEFAULT_ENABLE_CORS
                ),
            }
            sys.stdout.write(
                f"definitions.py is deprecated. Use {self.DEFINITION_FILE}\n\n"
            )
            return definition_data
        except ModuleNotFoundError as err:
            raise DefinitionException(f"Can not found {self.DEFINITION_FILE}") from err

    def __get_module_server(self, definitions):
        try:
            return definitions.SERVER
        except AttributeError as err:
            raise DefinitionException("SERVER is not defined") from err

    def __get_module_name(self, definitions, default_value):
        try:
            return definitions.NAME
        except AttributeError:
            return default_value

    def __get_module_version(self, definitions, default_value):
        try:
            return definitions.VERSION
        except AttributeError:
            return default_value

    def __get_module_debug(self, definitions, default_value):
        try:
            return definitions.DEBUG
        except AttributeError:
            return default_value

    def __get_module_cors(self, definitions, default_value):
        try:
            return definitions.ENABLE_CORS
        except AttributeError:
            return default_value


class DefinitionException(Exception):
    def __init__(self, message) -> None:
        self.message = message
