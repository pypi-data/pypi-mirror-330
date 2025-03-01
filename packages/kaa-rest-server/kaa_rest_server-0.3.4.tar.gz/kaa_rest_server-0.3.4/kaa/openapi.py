import ast
import importlib
import inspect

from .kaa_definition import KaaDefinition


class OpenApi:
    OPEN_API_VERSION = "3.0.3"

    def generate(self, kaa):
        definitions = KaaDefinition()
        elements = self.__get_elements(kaa)
        return {
            "openapi": self.OPEN_API_VERSION,
            "info": {
                "title": definitions.get_name(),
                "version": definitions.get_version(),
            },
            "paths": self.__get_paths(elements),
            # 'components': {
            #     'schemas': {
            #         'Default': {}
            #     }
            # }
        }

    def __get_elements(self, kaa):
        elements = []
        for module_name in kaa.resources:
            for class_name in kaa.resources[module_name]:
                elements.append(self.__fn(module_name, class_name))
        return elements

    def __get_paths(self, elements):
        paths = {}
        for element in elements:
            for operation_id in element:
                resource = element[operation_id]
                parameters = []

                if "path_params" in resource:
                    parameters += self.__path_params(resource["path_params"])
                if "query_params" in resource:
                    parameters += self.__query_params(resource["query_params"])

                method = resource["method"].lower()
                paths[resource["uri"]] = {
                    method: {
                        "operationId": operation_id,
                        "parameters": parameters,
                        "description": self.__get_val(
                            lambda v: v, resource, "description", ""
                        ),
                        "responses": {
                            "200": {
                                "description": "Response description",
                                "content": {"application/json": {}},
                                # '$ref': '#/components/schemas/Default'
                            }
                        },
                    }
                }
        return paths

    def __fn(self, module_name, class_name):
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        return get_decorators(class_)

    def __path_params(self, parameters):
        pm = []
        for k in parameters:
            parameter = parameters[k]
            p = {
                "name": k,
                "description": self.__get_val(
                    lambda v: v, parameter, "description", ""
                ),
                "in": "path",
                "schema": {
                    "type": self.__get_val(self.__get_type, parameter, "type", "string")
                },
                "required": True,
            }
            pm.append(p)
        return pm

    def __get_val(self, fn, item, key, default):
        return fn(item[key]) if key in item else default

    def __query_params(self, parameters):
        pm = []
        for k in parameters:
            parameter = parameters[k]
            p = {
                "name": k,
                "description": self.__get_val(
                    lambda v: v, parameter, "description", ""
                ),
                "in": "query",
                "schema": {
                    "type": self.__get_val(self.__get_type, parameter, "type", "string")
                },
                "required": self.__get_val(lambda v: v, parameter, "required", False),
            }
            pm.append(p)
        return pm

    def __get_type(self, param_type):
        if param_type == "int":
            return "integer"
        elif param_type == "float":
            return "number"
        return "string"


def get_decorators(cls):
    AVAILABLE_METHODS = ["GET", "PUT", "POST", "PATCH", "DELETE"]
    PATH = "PATH"
    AUTH = "AUTH"
    target = cls
    decorators = {}

    def visit_fn(node):
        if node.name[:2] == "__":
            return
        decorators[node.name] = {}
        for n in node.decorator_list:
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
                if name == PATH:
                    decorators[node.name].update(parse_path(n))
                elif name == AUTH:
                    decorators[node.name]["authorization"] = True
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id
                if name in AVAILABLE_METHODS:
                    decorators[node.name]["method"] = name

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_fn
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return decorators


def parse_path(node):
    result = {}

    def _parse(node):
        if isinstance(node, ast.AST):
            fields = [(a, b) for a, b in ast.iter_fields(node)]
            for field in fields:
                if field[0] == "args":
                    result.update(_parse_args(field[1]))
                elif field[0] == "keywords":
                    result.update(_parse_kw(field[1]))
                elif isinstance(field[1], ast.AST):
                    _parse(field[1])

    def _parse_args(node):
        if not isinstance(node, list):
            return {}
        childs = {}
        count = 0
        for child in node:
            count += 1
            if count == 1:
                childs["uri"] = _get_iter_fields(child)[0]
            if count == 2:
                childs["query_params"] = _parse_dict(child)
        return childs

    def _parse_kw(node):
        childs = {}
        for child in node:
            fields = _get_iter_fields(child)
            childs[fields[0]] = _parse_dict(fields[1])
        return childs

    def _parse_dict(node):
        params = []
        values = []
        for field_key, field_value in ast.iter_fields(node):
            if field_key == "keys":
                for k in field_value:
                    params += _get_iter_fields(k)
            elif field_key == "values":
                for k in field_value:
                    fields = _get_iter_fields(k)
                    if len(fields) == 1:
                        values.append(fields[0])
                    else:
                        values.append(_parse_dict(k))
            else:
                return field_value
        idx = 0
        result = {}
        for param in params:
            if param:
                result[param] = values[idx]
                idx += 1
        return result

    def _get_iter_fields(node):
        return [v for k, v in ast.iter_fields(node)]

    _parse(node)
    return result
