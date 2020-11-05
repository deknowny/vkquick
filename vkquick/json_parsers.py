"""
Имплементации `base/json_parser`
"""
import functools
import json

from vkquick.base.json_parser import JSONParser


class BuiltinJSONParser(JSONParser):
    """
    JSON парсер, использующий стандартную библиотеку
    """

    dumps = staticmethod(
        functools.partial(
            json.dumps, ensure_ascii=False, separators=(",", ":")
        )
    )
    loads = staticmethod(json.loads)
