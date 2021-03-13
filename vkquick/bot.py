import asyncio
import typing as ty

from vkquick.api import API
from vkquick.bases.event import Event
from vkquick.bases.events_factories import EventsFactory
from vkquick.handlers import EventHandler, SignalHandler


class Bot:
    def __init__(
        self, *,
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
        async with self._events_factory, self._api:
            await self._listen_events()

    async def _listen_events(self) -> ty.NoReturn:
        async for events in self._events_factory:
            for event in events:
                asyncio.create_task(self.pass_event_through_handlers(event))

    async def pass_event_through_handlers(self, event: Event):
        handling_coros = [handler(bot=self, event=event) for handler in self._event_handlers]
        await asyncio.gather(*handling_coros)