"""
Имплементации `bases/json_parser`
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


def route_to_proxy(value):
    if isinstance(value, list):
        return ListProxy(value)
    elif isinstance(value, dict):
        return DictProxy(value)
    else:
        return value


class DictProxy(dict):
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, "__use_super_getattribute", False)

    def __getattribute__(self, item):
        if item == "to_dict" or object.__getattribute__(self, "__use_super_getattribute"):
            return object.__getattribute__(self, item)

        return route_to_proxy(self[item])

    def to_dict(self):
        object.__setattr__(self, "__use_super_getattribute", True)
        return dict(self)


class ListProxy(list):
    def __getitem__(self, item):
        value = list.__getitem__(self, item)
        return route_to_proxy(value)


class BuiltinJsonParser(JSONParser):
    """
    JSON парсер, использующий стандартную библиотеку
    """

    @staticmethod
    def dumps(data: ty.Dict[str, ty.Any]) -> ty.Union[str, bytes]:
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    @staticmethod
    def loads(string: ty.Union[str, bytes]) -> DictProxy:
        return json.loads(string, object_hook=DictProxy)


class OrjsonParser(JSONParser):
    @staticmethod
    def dumps(data: ty.Dict[str, ty.Any]) -> ty.Union[str, bytes]:
        return orjson.dumps(data)  # pragma: no cover

    @staticmethod
    def loads(string: ty.Union[str, bytes]) -> DictProxy:
        return DictProxy(orjson.loads(string))  # pragma: no cover


class UjsonParser(JSONParser):
    @staticmethod
    def dumps(data: ty.Dict[str, ty.Any]) -> ty.Union[str, bytes]:
        return ujson.dumps(data, ensure_ascii=False)  # pragma: no cover

    @staticmethod
    def loads(string: ty.Union[str, bytes]) -> DictProxy:
        return ujson.loads(string, object_hook=DictProxy)  # pragma: no cover


# Значение этой переменной используется везде
if orjson is not None:
    json_parser_policy = OrjsonParser
elif ujson is not None:
    json_parser_policy = UjsonParser
else:
    json_parser_policy = BuiltinJsonParser
