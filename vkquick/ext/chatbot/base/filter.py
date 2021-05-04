from __future__ import annotations

import abc
import dataclasses
import typing as ty

# from vkquick.ext.chatbot.exceptions import FilterFailedError

if ty.TYPE_CHECKING:
    from vkquick.ext.chatbot.storages import NewMessage


class Filter(abc.ABC):
    @abc.abstractmethod
    async def make_decision(self, message_storage: NewMessage):
        ...

    def __or__(self, other: Filter) -> OrFilter:
        return OrFilter(self, other)

    def __and__(self, other: Filter) -> AndFilter:
        return AndFilter(self, other)


@dataclasses.dataclass
class OrFilter(Filter):

    filter1: Filter
    filter2: Filter

    async def make_decision(self, message_storage: NewMessage):
        try:
            await self.filter1.make_decision(message_storage)
        except FilterFailedError:
            await self.filter2.make_decision(message_storage)


@dataclasses.dataclass
class AndFilter(Filter):
    filter1: Filter
    filter2: Filter

    async def make_decision(self, message_storage: NewMessage):
        await self.filter1.make_decision(message_storage)
        await self.filter2.make_decision(message_storage)


class ShortcutFilter(Filter):
    def __init__(self, handler: ty.Callable[[NewMessage], ty.Awaitable]):
        self._handler = handler

    async def make_decision(self, message_storage: NewMessage):
        await self._handler(message_storage)


def filter(handler: ty.Callable[[NewMessage, ...], ty.Awaitable]) -> ty.Callable[..., ShortcutFilter]:
    def args_wrapper(*args, **kwargs):
        def func_replacement(message_storage: NewMessage):
            return handler(message_storage, *args, **kwargs)
        return ShortcutFilter(func_replacement)
    return args_wrapper


