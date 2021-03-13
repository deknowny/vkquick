from __future__ import annotations

import typing as ty

from loguru import logger

from vkquick.bases.event import Event
from vkquick.bases.filter import Filter
from vkquick.exceptions import FilterFailedError
from vkquick.sync_async import sync_async_run, sync_async_callable
from vkquick.json_parsers import DictProxy
from vkquick.bases.easy_decorator import EasyDecorator

if ty.TYPE_CHECKING:
    from vkquick.bot import Bot


class SignalHandler(EasyDecorator):
    def __init__(
        self,
        __handler: ty.Optional[ty.Callable] = None,
        *,
        name: ty.Optional[str] = None
    ):
        self._handler = __handler
        self._name = name or __handler.__name__

    def is_handling_name(self, name: str) -> bool:
        return self._name == name

    def __call__(self, *args, **kwargs):
        return self._handler(*args, **kwargs)


class EventHandlingContext:
    def __init__(
        self, *, bot: Bot, event: Event, extra: ty.Optional[DictProxy] = None
    ):
        self.bot = bot
        self.event = event
        self.extra = extra or DictProxy()
        self.filter_failed_exception = None
        self.handler_arguments = {}
        self.raised_exception_in_handler = None

    def add_handler_argument(self, **kwargs):
        self.handler_arguments.update(kwargs)


class EventHandler(EasyDecorator):
    def __init__(
        self,
        __handler: ty.Optional[ty.Callable] = None,
        *,
        handling_event_types: ty.Set[str] = None,
        filters: ty.List[Filter] = None,
        post_handling_callback: ty.Optional[
            sync_async_callable([EventHandlingContext])
        ] = None
    ):
        self._handler = __handler
        self._handling_event_types = handling_event_types or {
            __handler.__name__
        }
        self._filters = filters or []
        self._post_handling_callback = post_handling_callback

    def is_handling_event_type(self, event_type: str) -> bool:
        return event_type in self._handling_event_types

    def add_filter(self, filter: Filter) -> EventHandler:
        self._filters.append(filter)
        return self

    @logger.catch
    async def __call__(
        self, *, bot: Bot, event: Event
    ) -> EventHandlingContext:
        ehctx = EventHandlingContext(bot=bot, event=event,)
        if event.type not in self._handling_event_types:
            return ehctx
        await self.run_through_filters(ehctx)
        if ehctx.filter_failed_exception is not None:
            return ehctx

        await self.call_handler(ehctx)
        return ehctx

    async def run_through_filters(self, ehctx: EventHandlingContext) -> None:
        for filter_ in self._filters:
            try:
                await sync_async_run(filter_.make_decision(ehctx))
            except FilterFailedError as error:
                ehctx.filter_failed_exception = error
                await sync_async_run(filter_.handle_exception(ehctx))

    async def call_handler(self, ehctx: EventHandlingContext) -> None:
        try:
            return await sync_async_run(
                self._handler(**ehctx.handler_arguments)
            )
        except Exception as error:
            ehctx.raise_exception_in_handler = error
            raise error
