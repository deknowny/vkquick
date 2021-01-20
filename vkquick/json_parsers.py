"""
Имплементации `base/json_parser`
"""
import json
import typing as ty

from vkquick.base.json_parser import JSONParser

try:
    import orjson
except ImportError:  # pragma: no cover
    orjson = None


try:
    import ujson
except ImportError:  # pragma: no cover
    ujson = None


class BuiltinJsonParser(JSONParser):
    """
    JSON парсер, использующий стандартную библиотеку
    """

    @staticmethod
    def dumps(data: ty.Dict[str, ty.Any]) -> ty.Union[str, bytes]:
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    @staticmethod
    def loads(string: ty.Union[str, bytes]) -> ty.Dict[str, ty.Any]:
        return json.loads(string)


class OrjsonParser(JSONParser):
    @staticmethod
    def dumps(data: ty.Dict[str, ty.Any]) -> ty.Union[str, bytes]:
        return orjson.dumps(data)  # pragma: no cover

    @staticmethod
    def loads(string: ty.Union[str, bytes]) -> ty.Dict[str, ty.Any]:
        return orjson.loads(string)  # pragma: no cover


class UjsonParser(JSONParser):
    @staticmethod
    def dumps(data: ty.Dict[str, ty.Any]) -> ty.Union[str, bytes]:
        return ujson.dumps(data, ensure_ascii=False)  # pragma: no cover

    @staticmethod
    def loads(string: ty.Union[str, bytes]) -> ty.Dict[str, ty.Any]:
        return ujson.loads(string)  # pragma: no cover


# Значение этой переменной используется везде
if orjson is not None:
    json_parser_policy = OrjsonParser
elif ujson is not None:
    json_parser_policy = UjsonParser
else:
    json_parser_policy = BuiltinJsonParser
