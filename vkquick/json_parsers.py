"""
Имплементации разных JSON парсеров
"""
import json
import typing

from vkquick.base.json_parser import BaseJSONParser

try:
    import orjson
except ImportError:  # pragma: no cover
    orjson = None


try:
    import ujson
except ImportError:  # pragma: no cover
    ujson = None


class BuiltinJsonParser(BaseJSONParser):
    """
    JSON парсер, использующий стандартную библиотеку
    """

    @staticmethod
    def dumps(data: typing.Dict[str, typing.Any]) -> typing.Union[str, bytes]:
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    @staticmethod
    def loads(string: typing.Union[str, bytes]) -> typing.Any:
        return json.loads(string)


class OrjsonParser(BaseJSONParser):
    """
    JSON парсер, использующий `orjson`
    """

    @staticmethod
    def dumps(data: typing.Dict[str, typing.Any]) -> typing.Union[str, bytes]:
        return orjson.dumps(data)  # pragma: no cover

    @staticmethod
    def loads(string: typing.Union[str, bytes]) -> typing.Any:
        return orjson.loads(string)  # pragma: no cover


class UjsonParser(BaseJSONParser):
    """
    JSON парсер, использующий `ujson`
    """

    @staticmethod
    def dumps(data: typing.Dict[str, typing.Any]) -> typing.Union[str, bytes]:
        return ujson.dumps(data, ensure_ascii=False)  # pragma: no cover

    @staticmethod
    def loads(string: typing.Union[str, bytes]) -> typing.Any:
        return ujson.loads(string)  # pragma: no cover


json_parser_policy: typing.Type[BaseJSONParser]
"""
`json_parser_policy` -- установленный JSON парсер, используемый по умолчанию
"""

if orjson is not None:
    json_parser_policy = OrjsonParser
elif ujson is not None:
    json_parser_policy = UjsonParser
else:
    json_parser_policy = BuiltinJsonParser
