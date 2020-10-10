"""
Тривиальные инструменты для некоторых кейсов
"""
import asyncio
import random
import typing as ty


T = ty.TypeVar("T")


def peer(chat_id: int) -> int:
    """
    Добавляет к `chat_id` значение, чтобы оно стало `peer_id`.
    Кртакая и более приятная запись сложения любого числа с 2 000 000 000
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
    def __missing__(self, key):
        return "{" + key + "}"


class AttrDict:
    def __new__(cls, mapping):
        if isinstance(mapping, dict):
            self = object.__new__(cls)
            self.__init__(mapping)
            return self
        elif isinstance(mapping, list):
            return [cls(i) for i in mapping]

        else:
            return mapping

    def __init__(self, mapping):
        self.mapping_ = mapping

    def __getattr__(self, item):
        return self.__class__(self.mapping_[item])

    def __repr__(self):
        return f"{self.__class__.__name__}({self.mapping_})"

    def __call__(self, item):
        return self.__getattr__(item)

    def __getitem__(self, item):
        return self.mapping_[item]
