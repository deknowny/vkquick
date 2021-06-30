from __future__ import annotations

import abc
import dataclasses
import typing

from vkquick.chatbot.dependency import Depends, DependencyMixin
from vkquick.chatbot.exceptions import StopCurrentHandling

if typing.TYPE_CHECKING:  # pragma: no cover
    from vkquick.chatbot.storages import NewMessage

    OnErrorCallback = typing.Callable[[NewMessage], typing.Any]


class BaseFilter(abc.ABC):

    def __init__(self):
        self._on_error: typing.Optional[OnErrorCallback] = None
        self._dependency_mixin = DependencyMixin()
        self._dependency_mixin.parse_dependency_arguments(self.make_decision)

    async def run_making_decision(self, ctx: NewMessage):
        dependency_mapping = await self._dependency_mixin.make_dependency_arguments(ctx)
        try:
            return await self.make_decision(ctx, **dependency_mapping)
        except StopCurrentHandling as err:
            if self._on_error is not None:
                await self._on_error(ctx)
            raise err

    @abc.abstractmethod
    async def make_decision(self, ctx: NewMessage, **kwargs: Depends):
        """
        Метод, вызываемый для проверки корректности события

        Arguments:
            ctx: Контекст нового сообщения
            kwargs: Опциональные зависимости
        """

    async def on_error(self, func: OnErrorCallback):
        self._on_error = func

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
        except StopCurrentHandling:
            await self.filter2.make_decision(ctx)


@dataclasses.dataclass
class AndFilter(BaseFilter):
    filter1: BaseFilter
    filter2: BaseFilter

    async def make_decision(self, ctx: NewMessage):
        await self.filter1.make_decision(ctx)
        await self.filter2.make_decision(ctx)
