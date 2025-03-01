import importlib
from kaa import KaaServer, StartKaaError
from .kaa_definition import KaaDefinition


class Server:
    def __init__(self) -> None:
        definitions = KaaDefinition()
        server = definitions.get_server()
        spl = server.split(".")
        class_name = spl[-1]
        module_name = ".".join(spl[:-1])
        module = self.__get_module(module_name)
        class_ = getattr(module, class_name)
        self.server = class_()

    def __get_module(self, module_name):
        try:
            return importlib.import_module(module_name)
        except ImportError as err:
            raise StartKaaError(
                f"Module '{module_name}' is not defined.") from err

    def get_server(self) -> KaaServer:
        return self.server

    def serve(self, env, start_response):
        return self.server.serve(env, start_response)
