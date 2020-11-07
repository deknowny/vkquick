"""
Тривиальные инструменты для некоторых кейсов
(я просто не знаю, куда это деть)
"""
from __future__ import annotations
import asyncio
import enum
import json
import random
import os
import functools
import typing as ty

import pygments
import pygments.formatters
import pygments.lexers


T = ty.TypeVar("T")


def sync_async_callable(
    args: ty.Union[ty.List[ty.Any], type(...)], returns: ty.Any
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
    Случайное число в дипазоне +-`side`.
    Используется для API метода `messages.send`
    """
    return random.randint(-side, +side)


class SafeDict(dict):
    """
    Обертка для словаря, передаваемого в `str.format_map`
    (формат с возможными пропусками)
    """

    def __missing__(self, key):
        return "{" + key + "}"


class AttrDict():
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

    def __getattr__(self, item):
        return self.__class__(self()[item])

    def __repr__(self):
        return f"{self.__class__.__name__}({self.mapping_})"

    def __call__(self, item=None):
        if item is None:
            return self.mapping_
        return self.__getattr__(item)

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


def clear_console():
    """
    Очищает окно терминала
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class AutoLowerNameEnum(enum.Enum):
    """
    Enum, который при автоматически опускает
    имя ключа в нижний регистр и дает его в значение
    """

    @staticmethod
    def _generate_next_value_(name, *args):
        return name.lower()


class CustomEncoder(json.JSONEncoder):
    def default(self, obj: ty.Any) -> ty.Any:
        if isinstance(obj, AttrDict):
            return obj()
        return json.JSONEncoder.default(self, obj)


def pretty_view(mapping: dict) -> str:
    """
    Цветное отображение JSON словарей
    """
    scheme = json.dumps(mapping, ensure_ascii=False, indent=4, cls=CustomEncoder)
    scheme = pygments.highlight(
        scheme,
        pygments.lexers.JsonLexer(),  # noqa
        pygments.formatters.TerminalFormatter(bg="light"),  # noqa
    )
    return scheme
