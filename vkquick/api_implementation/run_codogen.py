"""
Codogen for all vk api
"""
import pathlib
import re

from vkquick.json_parsers import json_parser_policy


def load(fp: str):
    with open(pathlib.Path("vk-api-schema") / fp) as file:
        return json_parser_policy.loads(
            file.read()
        )


CLASS_TEMPLATE = """
class {method_header}(APIMethod):
    {methods}


""".lstrip()

METHOD_TEMPLATE = """
    @api_method
    async def {method_name}(
        self,{kw_only}
        {params}
        **kwargs
    ) -> {response}:
        \"""
        {docs}
        \"""
"""

PARAMS_TEMPLATE = """
{name}: {hint}{default},
""".strip()


DOCSTRING_TEMPLATE = """
{desc}{params_desc}
""".strip()

PARAM_DESC_TEMP = """
:param {name}: {desc}
""".strip()

def gen_methods():

    def to_snake_case(__name: str) -> str:
        return re.sub(
            r"(?P<let>[A-Z])",
            lambda match: f"_{match.group('let').lower()}",
            __name
        )

    methods = load("methods.json")
    with open("methods.py", "w+") as file:

        file.write(
            "import typing as ty\n\n"
            "import typing_extensions as tye\n\n"
            "from vkquick.api_implementation.base import APIMethod, api_method\n\n\n"

        )

        methods_temps = {}

        for method in methods["methods"]:
            header, name = method["name"].split(".")
            header = header.title()
            name = to_snake_case(name)

            # Build parameters
            params = []
            params_desc = []
            if "parameters" in method:
                for param in method["parameters"]:
                    param_name = param["name"]
                    if param_name in {"global"}:
                        param_name = param_name + "_"
                    if param["type"] == "integer":
                        param_type = "int"
                    elif param["type"] == "string":
                        param_type = "str"
                    elif param["type"] == "boolean":
                        param_type = "bool"
                    elif param["type"] == "number":
                        param_type = "float"

                    elif param["type"] == "array":
                        if param["items"].get("type") == "string":
                            if "enum" in param["items"]:
                                param_type = (
                                    f"ty.Sequence[tye.Literal["
                                    f"""{', '.join(map(repr, param['items']['enum']))}"""
                                    "]]"
                                )
                            else:
                                # Special for users.get
                                if "ids" in param["name"]:
                                    param_type = f"ty.List[ty.Union[str, int]]"
                                else:
                                    param_type = f"ty.List[str]"
                        elif "type" not in param["items"] and param["items"].get("format") == "json":

                            param_type = "dict"
                        else:
                            param_type = "ty.Sequence"

                    else:
                        param_type = "NONE"

                    if "default" in param:
                        if param["type"] == "array":
                            if param["items"].get("type") == "string":
                                param_default = f" = ({', '.join(param['default'].split(','))},)"
                            else:
                                param_default = f" = ()"
                        else:
                            param_default = f""" = {repr(param['default'])}"""
                    elif param.get("required"):
                        param_default = ""
                    else:
                        param_type = f"ty.Optional[{param_type}]"
                        param_default = " = None"

                    param_temp = PARAMS_TEMPLATE.format(
                        name=param_name,
                        hint=param_type,
                        default=param_default
                    )
                    param_desc_temp = PARAM_DESC_TEMP.format(
                        name=param_name,
                        desc=param.get("description") or "No description provided"
                    )
                    params.append(param_temp)
                    params_desc.append(param_desc_temp)

            if params_desc:
                params_desc = "\n\n\t\t" + "\n\t\t".join(params_desc)
            else:
                params_desc = ""
            docstring_temp = DOCSTRING_TEMPLATE.format(
                desc=method.get("description") or "No description provided",
                params_desc=params_desc
            )
            method_temp = METHOD_TEMPLATE.format(
                method_name=name,
                params="\n\t\t".join(params),
                response=1,
                docs=docstring_temp,
                kw_only=" *," if params else ""
            )

            if header in methods_temps:
                methods_temps[header].append(method_temp)
            else:
                methods_temps[header] = [method_temp]

        for method_header, methods in methods_temps.items():
            class_methods = "".join(methods)
            class_temp = CLASS_TEMPLATE.format(
                method_header=method_header,
                methods=class_methods
            )

            file.write(class_temp.replace("\t", " "*4).replace("'", '"'))



OBJECT_CLASS_TEMPLATE = """
class {name}(APIObject):
    {fields}
""".lstrip()

OBJECT_PROPERTY_TEMPLATE = """
@property
def {name}(self) -> {hint}:
    \"""
    {desc}
    \"""
    return self.__schema__["{name}"]
"""

def gen_objects():
    objects = load("objects.json")

    with open("objects.py", "w+") as file:
        file.write(
            "from __future__ import annotations\n\n"
            "import enum\n"
            "import typing as ty\n\n"
            "import typing_extensions as tye\n\n"
            "from vkquick.api_implementation.base import APIObject\n\n\n"

        )
        for entity in objects["definitions"]:
            if entity["type"] == "object":
                fields = []
                for field_name, field in entity["properties"].items():
                    field_name = field
                    # Later





def main():
    gen_methods()
    gen_objects()


if __name__ == '__main__':
    main()