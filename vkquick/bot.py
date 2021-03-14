from __future__ import annotations
import asyncio
import dataclasses
import typing as ty

from vkquick.api import API
from vkquick.bases.event import Event
from vkquick.bases.events_factories import EventsFactory
from vkquick.sync_async import sync_async_run

if ty.TYPE_CHECKING:
    from vkquick.signal_handler import SignalHandler
    from vkquick.event_handler.handler import EventHandler


@dataclasses.dataclass
class EventProcessingContext:
    bot: Bot
    event: Event
    extra: dict = dataclasses.field(default_factory=dict)


class Bot:
    def __init__(
        self,
        *,
        api: API,
        events_factory: EventsFactory,
        event_handlers: ty.Optional[ty.List[EventHandler]] = None,
        signal_handlers: ty.Optional[ty.List[SignalHandler]] = None
    ):
        self._api = api
        self._events_factory = events_factory
        self._event_handlers = event_handlers or []
        self._signal_handlers = signal_handlers or []

    @property
    def api(self) -> API:
        return self._api

    @property
    def events_factory(self) -> EventsFactory:
        return self._events_factory

    def run(self) -> ty.NoReturn:
        asyncio.run(self.async_run())

    async def async_run(self) -> ty.NoReturn:
        try:
            await sync_async_run(self.call_signal("startup", self))
            async with self._events_factory, self._api:
                await self._listen_events()
        finally:
            await sync_async_run(self.call_signal("shutdown", self))

    async def _listen_events(self) -> ty.NoReturn:
        async for events in self._events_factory:
            for event in events:
                epctx = EventProcessingContext(bot=self, event=event)
                asyncio.create_task(self.pass_event_through_handlers(epctx))

    async def pass_event_through_handlers(self, epctx: EventProcessingContext):
        handling_coros = [
            handler(epctx) for handler in self._event_handlers
        ]
        await asyncio.gather(*handling_coros)

    def call_signal(self, __name: str, *args, **kwargs):
        for signal_handler in self._signal_handlers:
            if signal_handler.is_handling_name(__name):
                return signal_handler(*args, **kwargs)
