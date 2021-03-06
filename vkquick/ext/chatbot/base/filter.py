from __future__ import annotations

import abc
import dataclasses
import typing as ty

from vkquick.ext.chatbot.exceptions import FilterFailedError

if ty.TYPE_CHECKING:
    from vkquick.ext.chatbot.storages import NewMessage


class BaseFilter(abc.ABC):
    @abc.abstractmethod
    async def make_decision(self, ctx: NewMessage):
        ...

    def __or__(self, other: BaseFilter) -> OrFilter:
        return OrFilter(self, other)

    def __and__(self, other: BaseFilter) -> AndFilter:
        return AndFilter(self, other)


@dataclasses.dataclass
class OrFilter(BaseFilter):

    filter1: BaseFilter
    filter2: BaseFilter

    async def make_decision(self, ctx: NewMessage):
        try:
            await self.filter1.make_decision(ctx)
        except FilterFailedError:
            await self.filter2.make_decision(ctx)


@dataclasses.dataclass
class AndFilter(BaseFilter):
    filter1: BaseFilter
    filter2: BaseFilter

    async def make_decision(self, ctx: NewMessage):
        await self.filter1.make_decision(ctx)
        await self.filter2.make_decision(ctx)


@dataclasses.dataclass
class ShortcutFilter(BaseFilter):

    handler: ty.Callable[[NewMessage], ty.Awaitable]

    async def make_decision(self, ctx: NewMessage):
        await self.handler(ctx)


def filter(
    handler: ty.Callable[[NewMessage, ...], ty.Awaitable]
) -> ty.Callable[..., ShortcutFilter]:
    def args_wrapper(*args, **kwargs):
        def func_replacement(ctx: NewMessage):
            return handler(ctx, *args, **kwargs)

        return ShortcutFilter(func_replacement)

    return args_wrapper
