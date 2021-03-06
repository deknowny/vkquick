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


def create_aiohttp_session():
    return aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False),
        skip_auto_headers={"User-Agent"},
        raise_for_status=True,
        json_serialize=json_parser_policy.dumps,
    )

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


# Copied from `pyramid`
class cached_property:
    """Use as a class method decorator.  It operates almost exactly like the
    Python ``@property`` decorator, but it puts the result of the method it
    decorates into the instance dict after the first call, effectively
    replacing the function it decorates with an instance variable.  It is, in
    Python parlance, a non-data descriptor.  The following is an example and
    its usage:
    .. doctest::
        >>> from pyramid.decorator import reify
        >>> class Foo:
        ...     @reify
        ...     def jammy(self):
        ...         print('jammy called')
        ...         return 1
        >>> f = Foo()
        >>> v = f.jammy
        jammy called
        >>> print(v)
        1
        >>> f.jammy
        1
        >>> # jammy func not called the second time; it replaced itself with 1
        >>> # Note: reassignment is possible
        >>> f.jammy = 2
        >>> f.jammy
        2
    """

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.__doc__ = wrapped.__doc__

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        # reify is a non-data-descriptor which is leveraging the fact
        # that it is not invoked if the equivalent attribute is defined in the
        # object's dict, so the setattr here effectively hides this descriptor
        # from subsequent lookups
        setattr(inst, self.wrapped.__name__, val)
        return val