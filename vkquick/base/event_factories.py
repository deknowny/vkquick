from __future__ import annotations

import abc
import asyncio
import typing

import aiohttp
from loguru import logger

from vkquick.base.event import BaseEvent
from vkquick.base.json_parser import BaseJSONParser
from vkquick.base.session_container import SessionContainerMixin
from vkquick.pretty_view import pretty_view

if typing.TYPE_CHECKING:  # pragma: no cover
    from vkquick.api import API


EventsCallback = typing.Callable[[BaseEvent], typing.Awaitable[None]]


class BaseEventFactory(SessionContainerMixin, abc.ABC):

    _api: API
    _new_event_callbacks: typing.List[EventsCallback]

    def __init__(
        self,
        *,
        api: API,
        new_event_callbacks: typing.Optional[
            typing.List[EventsCallback]
        ] = None,
        requests_session: typing.Optional[aiohttp.ClientSession] = None,
        json_parser: typing.Optional[BaseJSONParser] = None,
    ):
        self._api = api
        self._new_event_callbacks = new_event_callbacks or []
        SessionContainerMixin.__init__(
            self, requests_session=requests_session, json_parser=json_parser
        )

    @abc.abstractmethod
    async def _coroutine_run_polling(self):
        ...

    async def listen(
        self, same_poll: bool = False
    ) -> typing.AsyncGenerator[BaseEvent, None]:
        events_queue: asyncio.Queue[BaseEvent] = asyncio.Queue()
        logger.debug("Run events listening")
        try:
            self.add_event_callback(events_queue.put)
            if not same_poll:
                asyncio.create_task(self.coroutine_run_polling())
            while True:
                yield await events_queue.get()

        finally:
            logger.debug("End events listening")
            self.remove_event_callback(events_queue.put)

    def add_event_callback(self, func: EventsCallback) -> EventsCallback:
        logger.debug("Add event callback: {func}", func=func)
        self._new_event_callbacks.append(func)
        return func

    def remove_event_callback(self, func: EventsCallback) -> EventsCallback:
        logger.debug("Remove event callback: {func}", func=func)
        self._new_event_callbacks.remove(func)
        return func

    async def coroutine_run_polling(self) -> None:
        logger.info(
            "Run {polling_type} polling", polling_type=self.__class__.__name__
        )
        try:
            await self._coroutine_run_polling()
        finally:
            logger.info(
                "End {polling_type} polling",
                polling_type=self.__class__.__name__,
            )

    async def _run_through_callbacks(self, event: BaseEvent) -> None:
        logger.debug(
            "New event: {event}",
            event=event,
        )
        logger.opt(lazy=True).debug(
            "Event content: {event_content}",
            event_content=lambda: pretty_view(event.content),
        )
        updates = [callback(event) for callback in self._new_event_callbacks]
        await asyncio.gather(*updates)

    def run_polling(self):
        asyncio.run(self.coroutine_run_polling())


class BaseLongPoll(BaseEventFactory):
    def __init__(
        self,
        *,
        api: API,
        event_wrapper: typing.Type[BaseEvent],
        new_event_callbacks: typing.Optional[
            typing.List[EventsCallback]
        ] = None,
        requests_session: typing.Optional[aiohttp.ClientSession] = None,
        json_parser: typing.Optional[BaseJSONParser] = None,
    ):
        self._event_wrapper = event_wrapper
        self._baked_request: typing.Optional[typing.Awaitable] = None
        self._requests_query_params: typing.Optional[dict] = None
        self._server_url: typing.Optional[str] = None

        BaseEventFactory.__init__(
            self,
            api=api,
            new_event_callbacks=new_event_callbacks,
            requests_session=requests_session,
            json_parser=json_parser,
        )

    @abc.abstractmethod
    async def _setup(self) -> None:
        """
        Обновляет или получает информацию о LongPoll сервере
        и открывает соединение
        """

    async def _coroutine_run_polling(self) -> None:
        await self._setup()
        self._requests_query_params = typing.cast(
            dict, self._requests_query_params
        )
        self._update_baked_request()
        self._baked_request = typing.cast(asyncio.Task, self._baked_request)

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
                        response = await self.parse_json_body(response)
                        if "updates" not in response:
                            await self._resolve_faileds(response)
                            continue
                    else:
                        response = await self.parse_json_body(response)
                        await self._resolve_faileds(response)
                        continue

                if not response["updates"]:
                    continue

                for update in response["updates"]:
                    event = self._event_wrapper(update)
                    asyncio.create_task(self._run_through_callbacks(event))

    async def _resolve_faileds(self, response: dict):
        self._requests_query_params = typing.cast(
            dict, self._requests_query_params
        )
        if response["failed"] == 1:
            self._requests_query_params.update(ts=response["ts"])
        elif response["failed"] in (2, 3):
            await self._setup()
        else:
            raise ValueError("Invalid longpoll version")

        self._update_baked_request()

    def _update_baked_request(self) -> None:
        self._server_url = typing.cast(str, self._server_url)
        self._baked_request = self.requests_session.get(
            self._server_url, params=self._requests_query_params
        )
        self._baked_request = asyncio.create_task(self._baked_request)

    async def close_session(self) -> None:
        await self._api.close_session()
        await BaseEventFactory.close_session(self)
