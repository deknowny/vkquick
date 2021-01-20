"""
Тривиальные инструменты для некоторых кейсов
(я просто не знаю, куда это деть)
"""
from __future__ import annotations

import asyncio
import datetime
import functools
import json
import os
import random
import re
import warnings
import multiprocessing
import typing as ty

import aiohttp
import pygments
import pygments.formatters
import pygments.lexers

from vkquick.json_parsers import json_parser_policy

T = ty.TypeVar("T")


def sync_async_callable(
    args: ty.Union[ty.List[ty.Any], type(...)], returns: ty.Any = ty.Any
) -> ty.Type[ty.Callable]:
    if args is not Ellipsis:
        return ty.Callable[
            [*args], ty.Union[ty.Awaitable[returns], returns],
        ]

    return ty.Callable[
        ..., ty.Union[ty.Awaitable[returns], returns],
    ]


@functools.lru_cache(maxsize=None)
def peer(chat_id: int = 0) -> int:
    """
    Добавляет к `chat_id` значение, чтобы оно стало `peer_id`.
    Краткая и более приятная запись сложения любого числа с 2 000 000 000
    (да, на один символ)

    peer_id=vq.peer(123)
    """
    return 2_000_000_000 + chat_id


async def sync_async_run(
    obj: ty.Union[T, ty.Awaitable]
) -> ty.Union[T, ty.Any]:
    """
    Если `obj` является корутинным объектом --
    применится `await`. В ином случае, вернется само переданное значение
    """
    if asyncio.iscoroutine(obj):
        return await obj
    return obj


def random_id(side: int = 2 ** 31 - 1) -> int:
    """
    Случайное число в диапазоне +-`side`.
    Используется для API метода `messages.send`
    """
    return random.randint(-side, +side)


class SafeDict(dict):
    """
    Обертка для словаря, передаваемого в `str.format_map`
    (формат с возможными пропусками)
    """

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def _key_check(func):
    @functools.wraps(func)
    def wrapper(self, item):
        try:
            return func(self, item)
        except KeyError as err:
            available_keys = tuple(self().keys())
            raise KeyError(
                f"There isn't a key `{item}` in keys {available_keys}"
            ) from err

    return wrapper


class AttrDict:
    """
    Надстройка к словарю для возможности получения
    значений через точку. Работает рекурсивно,
    поддержка списков также имеется.

        foo = AttrDict({"a": {"b": 1}})
        print(foo.a.b)  # 1

        foo = AttrDict([{"a": [{"b": 1}]}])
        print(foo[0].a[0].b)  # 1

        # Когда ключ нельзя получить через атрибут
        foo = AttrDict({"#$@234": 1})
        print(foo("#$@234"))  # 1

        # Нужно получить исходный объект
        foo = AttrDict({"a": 1})
        print(foo())  # {'a': 1}

        foo = AttrDict({})
        foo.a = 1  # foo["a"] = 1
        print(foo())  # {'a': 1}

        # `__getitem__` возвращает исходный объект.
        # `__call__` -- новую обертку AttrDict
        foo = AttrDict({"a": {"b": 1}})
        print(isinstance(foo.a, AttrDict))  # True
        print(isinstance(foo["a"], dict))  # True
    """

    def __new__(cls, mapping=None):
        if mapping is None:
            mapping = {}
        if isinstance(mapping, (dict, list)):
            self = object.__new__(cls)
            self.__init__(mapping)
            return self

        return mapping

    def __init__(self, mapping=None):
        if mapping is None:
            mapping = {}
        object.__setattr__(self, "mapping_", mapping)

    @_key_check
    def __getattr__(self, item):
        return self.__class__(self()[item])

    def __repr__(self):
        return f"{self.__class__.__name__}({self.mapping_})"

    def __call__(self, item=None):
        if item is None:
            return self.mapping_
        return self.__getattr__(item)

    @_key_check
    def __getitem__(self, item):
        val = self.mapping_[item]
        if isinstance(self.mapping_, list):
            return self.__class__(val)
        return self.mapping_[item]

    def __contains__(self, item):
        return item in self.mapping_

    def __setattr__(self, key, value):
        self.mapping_[key] = value

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __len__(self):
        return len(self())

    def __bool__(self):
        return bool(self())

    def __eq__(self, other):
        return self() == other


def clear_console():
    """
    Очищает окно терминала
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class _CustomEncoder(json.JSONEncoder):
    def default(self, obj: ty.Any) -> ty.Any:
        if isinstance(obj, AttrDict):
            return obj()
        return super().default(obj)  # pragma: no cover


def pretty_view(mapping: ty.Union[dict, AttrDict]) -> str:
    """
    Цветное отображение JSON словарей
    """
    scheme = json.dumps(
        mapping, ensure_ascii=False, indent=4, cls=_CustomEncoder
    )
    scheme = pygments.highlight(
        scheme,
        pygments.lexers.JsonLexer(),  # noqa
        pygments.formatters.TerminalFormatter(bg="light"),  # noqa
    )
    return scheme


async def download_file(url: str) -> bytes:
    """
    Скачивание файлов по их прямой ссылке
    """
    session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False),
        skip_auto_headers={"User-Agent"},
        raise_for_status=True,
        json_serialize=json_parser_policy.dumps,
    )
    async with session.get(url) as response:
        return await response.read()


_registration_date_regex = re.compile('ya:created dc:date="(?P<date>.*?)"')


async def get_user_registration_date(
    id_: int, *, session: ty.Optional[aiohttp.ClientSession] = None
) -> datetime.datetime:
    request_session = session or aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False),
        skip_auto_headers={"User-Agent"},
        raise_for_status=True,
        json_serialize=json_parser_policy.dumps,
    )
    async with request_session:
        async with request_session.get(
            "https://vk.com/foaf.php", params={"id": id_}
        ) as response:
            user_info = await response.text()
            registration_date = _registration_date_regex.search(user_info)
            if registration_date is None:
                raise ValueError(f"No such user with id `{id_}`")
            registration_date = registration_date.group("date")
            registration_date = datetime.datetime.fromisoformat(
                registration_date
            )
            return registration_date


def mark_positional_only(*positional_args_name):
    def func_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for arg_name in positional_args_name:
                if arg_name in kwargs:
                    # Copied the original exception text
                    warnings.warn(
                        f"{func.__name__}() got some"
                        f"positional-only arguments"
                        f"passed as keyword arguments: "
                        f"{arg_name!r}. Pass the "
                        f"argument without its name."
                    )
            return func(*args, **kwargs)

        return wrapper

    return func_decorator


# Copied from built-in module functools (python3.8 required)

_NOT_FOUND = object()


class cached_property:
    def __init__(self, func):
        self.func = func
        self.attrname = None
        self.__doc__ = func.__doc__
        self.lock = multiprocessing.RLock()

    def __set_name__(self, owner, name):
        if self.attrname is None:
            self.attrname = name
        elif name != self.attrname:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                f"({self.attrname!r} and {name!r})."
            )

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.attrname is None:
            raise TypeError(
                "Cannot use cached_property instance without calling __set_name__ on it."
            )
        try:
            cache = instance.__dict__
        except AttributeError:  # not all objects have __dict__ (e.g. class defines slots)
            msg = (
                f"No '__dict__' attribute on {type(instance).__name__!r} "
                f"instance to cache {self.attrname!r} property."
            )
            raise TypeError(msg) from None
        val = cache.get(self.attrname, _NOT_FOUND)
        if val is _NOT_FOUND:
            with self.lock:
                # check if another thread filled cache while we awaited lock
                val = cache.get(self.attrname, _NOT_FOUND)
                if val is _NOT_FOUND:
                    val = self.func(instance)
                    try:
                        cache[self.attrname] = val
                    except TypeError:
                        msg = (
                            f"The '__dict__' attribute on {type(instance).__name__!r} instance "
                            f"does not support item assignment for caching {self.attrname!r} property."
                        )
                        raise TypeError(msg) from None
        return val
