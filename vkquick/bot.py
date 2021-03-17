from __future__ import annotations
import asyncio
import dataclasses
import functools
import typing as ty

from vkquick.api import API
from vkquick.longpoll import UserLongPoll, GroupLongPoll
from vkquick.bases.event import Event
from vkquick.bases.easy_decorator import easy_method_decorator
from vkquick.bases.events_factories import EventsFactory
from vkquick.event_handler.handler import EventHandler
from vkquick.signal_handler import SignalHandler
from vkquick.event_handler.context import EventHandlingContext
from vkquick.sync_async import sync_async_run, sync_async_callable, run_as_sync

if ty.TYPE_CHECKING:
    from vkquick import Filter
    from vkquick.bases.middleware import Middleware


def _adding_method_decorator(factory):
    def wrapper(method):
        @easy_method_decorator
        @functools.wraps(method)
        def method(self, __handler, **kwargs):
            if not isinstance(__handler, factory):
                __handler = factory(__handler, **kwargs)
            self._event_handlers.append(__handler)
            return __handler

        return method

    return wrapper


@dataclasses.dataclass
class EventProcessingContext:
    bot: Bot
    event: Event
    event_handling_contexts: ty.List[
        EventHandlingContext
    ] = dataclasses.field(default_factory=list)
    extra: dict = dataclasses.field(default_factory=dict)


class Bot:
    def __init__(
        self,
        *,
        api: API,
        events_factory: EventsFactory,
        event_handlers: ty.Optional[ty.List[EventHandler]] = None,
        signal_handlers: ty.Optional[ty.List[SignalHandler]] = None,
        middlewares: ty.Optional[ty.List[Middleware]] = None
    ):
        self._api = api
        self._events_factory = events_factory
        self._event_handlers = event_handlers or []
        self._signal_handlers = signal_handlers or []
        self._middlewares = middlewares or []

    @classmethod
    def via_token(cls, token: str, **kwargs):

        api = API(token)
        owner = run_as_sync(api.fetch_token_owner_entity())
        if owner.is_group:
            lp = GroupLongPoll(api)
        else:
            lp = UserLongPoll(api)

        return cls(api=api, events_factory=lp, **kwargs)

    @property
    def api(self) -> API:
        return self._api

    @property
    def events_factory(self) -> EventsFactory:
        return self._events_factory

    @property
    def event_handlers(self) -> ty.List[EventHandler]:
        return self._event_handlers

    @property
    def signal_handlers(self) -> ty.List[SignalHandler]:
        return self._signal_handlers

    @property
    def middlewares(self) -> ty.List[Middleware]:
        return self._middlewares

    def run(self) -> ty.NoReturn:
        asyncio.run(self.coroutine_run())

    async def coroutine_run(self) -> ty.NoReturn:
        try:
            await sync_async_run(self.call_signal("startup", self))
            async with self._events_factory, self._api:
                await self.listen_events()
        finally:
            await sync_async_run(self.call_signal("shutdown", self))

    async def listen_events(self) -> ty.NoReturn:
        async for event in self._events_factory.listen():
            epctx = EventProcessingContext(bot=self, event=event)
            asyncio.create_task(self._route_context(epctx))

    async def _route_context(self, epctx: EventProcessingContext):
        await self._call_forward_middlewares(epctx)
        await self._pass_context_through_handlers(epctx)
        await self._call_afterword_middlewares(epctx)

    async def _pass_context_through_handlers(
        self, epctx: EventProcessingContext
    ):
        handling_coros = []
        for handler in self._event_handlers:
            ehctx = EventHandlingContext(epctx=epctx)
            epctx.event_handling_contexts.append(ehctx)
            handling_coros.append(handler(ehctx=ehctx))
        await asyncio.gather(*handling_coros)

    def call_signal(self, __name: str, *args, **kwargs):
        for signal_handler in self._signal_handlers:
            if signal_handler.is_handling_name(__name):
                return signal_handler(*args, **kwargs)

    async def _call_forward_middlewares(self, epctx: EventProcessingContext):
        for middleware in self._middlewares:
            await sync_async_run(middleware.foreword(epctx))

    async def _call_afterword_middlewares(
        self, epctx: EventProcessingContext
    ):
        for middleware in reversed(self._middlewares):
            await sync_async_run(middleware.afterword(epctx))

    @_adding_method_decorator(EventHandler)
    def add_event_handler(
        self,
        __handler: ty.Optional[ty.Callable] = None,
        *,
        handling_event_types: ty.Set[str] = None,
        filters: ty.List[Filter] = None,
        post_handling_callbacks: ty.Optional[
            ty.List[sync_async_callable([EventHandlingContext])]
        ] = None,
        pass_ehctx_as_argument: bool = True,
        **kwargs
    ):
        ...

    @_adding_method_decorator(SignalHandler)
    def add_signal_handler(
        self,
        __handler: ty.Optional[ty.Callable] = None,
        *,
        name: ty.Optional[str] = None,
        **kwargs
    ):
        ...

    @easy_method_decorator
    def add_signal_handler(self, __handler: ty.Optional[Middleware] = None):
        self._middlewares.append(__handler)
