from __future__ import annotations

import abc
import asyncio
import typing as ty

import aiohttp
from loguru import logger

from vkquick.bases.json_parser import JSONParser
from vkquick.bases.session_container import SessionContainerMixin
from vkquick.event import Event

if ty.TYPE_CHECKING:
    from vkquick.api import API


EventsCallback = ty.Callable[[Event], ty.Awaitable[None]]


class EventsFactory(abc.ABC):
    """ """

    def __init__(
        self,
        *,
        api: API,
        new_event_callbacks: ty.List[EventsCallback] = None,
    ):
        self._api = api
        self._new_event_callbacks = new_event_callbacks or []

    async def listen(self) -> ty.AsyncGenerator[Event, None]:
        gen = self._listen()
        logger.info("Run polling (#{id:x})", id=id(gen))
        try:
            async for event in gen:
                logger.info(
                    "New event {event} (#{id:x}) from polling (#{id_polling:x})",
                    event=event,
                    id=id(event),
                    id_polling=id(gen),
                )
                logger.debug(
                    "Event content: {event_content}",
                    event_content=event.content,
                )
                yield event
        finally:
            logger.info("End polling (#{id:x})", id=id(gen))

    @abc.abstractmethod
    def _listen(self) -> ty.AsyncGenerator[Event, None]:
        """ """
        ...

    @property
    def api(self) -> API:
        """ """
        return self._api

    def add_event_callback(self, func: EventsCallback) -> EventsCallback:
        """

        Args:
          func: EventsCallback:
          func: EventsCallback:

        Returns:

        """
        logger.info("Add event callback {func}", func=func)
        self._new_event_callbacks.append(func)
        return func

    def remove_event_callback(self, func: EventsCallback) -> EventsCallback:
        """

        Args:
          func: EventsCallback:
          func: EventsCallback:

        Returns:

        """
        self._new_event_callbacks.remove(func)
        return func

    async def sublisten(self) -> ty.AsyncGenerator[Event, None]:
        events_queue = asyncio.Queue()
        logger.info("Run events sublistening (#{id:x})", id=id(events_queue))
        callback = events_queue.put

        try:
            self.add_event_callback(callback)
            while True:
                yield await events_queue.get()

        finally:
            logger.info(
                "End events sublistening (#{id:x})", id=id(events_queue)
            )
            self.remove_event_callback(callback)

    async def coroutine_run(self):
        async for _ in self.listen():
            pass

    def run(self):
        """ """
        asyncio.run(self.coroutine_run())

    async def _run_through_callbacks(self, event: Event) -> None:
        updates = [callback(event) for callback in self._new_event_callbacks]
        await asyncio.gather(*updates)


class LongPollBase(SessionContainerMixin, EventsFactory):
    """Базовый интерфейс для всех типов LongPoll"""

    def __init__(
        self,
        *,
        api: API,
        event_wrapper: ty.Type[Event],
        new_event_callbacks: ty.Optional[ty.List[EventsCallback]] = None,
        requests_session: ty.Optional[aiohttp.ClientSession] = None,
        json_parser: ty.Optional[JSONParser] = None,
    ):
        self._event_wrapper = event_wrapper
        self._baked_request: ty.Optional[asyncio.Task] = None
        self._requests_query_params: ty.Optional[dict] = None
        self._server_url: ty.Optional[str] = None

        EventsFactory.__init__(
            self, api=api, new_event_callbacks=new_event_callbacks
        )
        SessionContainerMixin.__init__(
            self, requests_session=requests_session, json_parser=json_parser
        )

    @abc.abstractmethod
    async def _setup(self) -> None:
        """
        Обновляет или получает информацию о LongPoll сервере
        и открывает соединение
        """

    async def _listen(self) -> ty.AsyncGenerator[Event, None]:
        await self._setup()
        self._update_baked_request()

        while True:
            try:
                response = await self._baked_request
            except asyncio.TimeoutError:
                self._update_baked_request()
                continue
            else:
                async with response:
                    if "X-Next-Ts" in response.headers:
                        self._requests_query_params.update(
                            ts=response.headers["X-Next-Ts"]
                        )
                        self._update_baked_request()
                        response = await self._parse_json_body(response)
                    else:
                        response = await self._parse_json_body(response)
                        await self._resolve_faileds(response)
                        self._update_baked_request()
                        continue

                if not response["updates"]:
                    continue

                for update in response["updates"]:
                    event = self._event_wrapper(update)
                    asyncio.create_task(self._run_through_callbacks(event))
                    yield event

    async def _resolve_faileds(self, response: dict):
        """
        Обрабатывает LongPoll ошибки (faileds)
        """
        if response["failed"] == 1:
            self._requests_query_params.update(ts=response["ts"])
        elif response["failed"] in (2, 3):
            await self._setup()
        else:
            raise ValueError("Invalid longpoll version")

    def _update_baked_request(self) -> None:
        """ """
        self._baked_request = self.requests_session.get(
            self._server_url, params=self._requests_query_params
        )
        self._baked_request = asyncio.create_task(self._baked_request)

    async def close_session(self) -> None:
        await self._api.close_session()
        await SessionContainerMixin.close_session(self)
