"""
Имплементации разных JSON парсеров
"""
import json
import typing as ty

from vkquick.bases.json_parser import JSONParser

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
    def loads(string: ty.Union[str, bytes]) -> ty.Any:
        return json.loads(string)


class OrjsonParser(JSONParser):
    """
    JSON парсер, использующий `orjson`
    """

    @staticmethod
    def dumps(data: ty.Dict[str, ty.Any]) -> ty.Union[str, bytes]:
        return orjson.dumps(data)  # pragma: no cover

    @staticmethod
    def loads(string: ty.Union[str, bytes]) -> ty.Any:
        return orjson.loads(string)  # pragma: no cover


class UjsonParser(JSONParser):
    """
    JSON парсер, использующий `ujson`
    """

    @staticmethod
    def dumps(data: ty.Dict[str, ty.Any]) -> ty.Union[str, bytes]:
        return ujson.dumps(data, ensure_ascii=False)  # pragma: no cover

    @staticmethod
    def loads(string: ty.Union[str, bytes]) -> ty.Any:
        return ujson.loads(string)  # pragma: no cover


# `json_parser_policy` -- установленный JSON парсер, используемый по умолчанию
if orjson is not None:
    json_parser_policy: ty.Type[JSONParser] = OrjsonParser
elif ujson is not None:
    json_parser_policy: ty.Type[JSONParser] = UjsonParser
else:
    json_parser_policy: ty.Type[JSONParser] = BuiltinJsonParser
