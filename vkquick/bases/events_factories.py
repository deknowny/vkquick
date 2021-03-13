import abc
import asyncio
import typing as ty

import aiohttp
from vkquick.api import API
from vkquick_old.events_factories.longpoll import Callback


class LongPollBase(AiohttpSessionContainer, abc.ABC):
    """
    Базовый интерфейс для всех типов LongPoll
    """

    _lp_requests_settings: ty.Optional[ty.Optional[dict]] = None
    _server_url: ty.Optional[str] = None
    _api: ty.Optional[API] = None
    _event_wrapper: ty.Optional[ty.Type[Event]] = None
    _baked_request = None

    def __init__(
        self, *,
        new_event_callbacks: ty.Optional[ty.List[ty.Coroutine[[Event], None, None]]] = None,
        requests_session: ty.Optional[aiohttp.ClientSession] = None,
        json_parser: ty.Optional[JSONParser] = None
    ):
        super().__init__(requests_session=requeserequests_session, json_parser=json_parser)
        self._new_event_callbacks = new_event_callbacks


    @abc.abstractmethod
    async def _setup(self) -> None:
        """
        Обновляет или получает информацию о LongPoll сервере
        и открывает соединение
        """

    def __aiter__(self) -> LongPollBase:
        """
        Итерация запускает процесс получения событий
        """
        self._setup_called = False
        return self

    async def __anext__(self,) -> ty.List[Event]:
        """
        Отправляет запрос на LongPoll сервер и ждет событие.
        После оборачивает событие в специальную обертку, которая
        в некоторых случаях может сделать интерфейс
        пользовательского лонгпула аналогичным групповому
        """
        if not self._setup_called:
            await self._setup()
            self._setup_called = True
            self._update_baked_request()

        response = await self._baked_request
        async with response:
            if "X-Next-Ts" in response.headers:
                self._lp_requests_settings.update(
                    ts=response.headers["X-Next-Ts"]
                )
                self._update_baked_request()
                response = await self._parse_json_body(response)
            else:
                response = await self._parse_json_body(response)
                await self._resolve_faileds(response)
                self._update_baked_request()
                return []

        updates = [
            self._event_wrapper(update)
            for update in response["updates"]
        ]
        asyncio.create_task(self._run_through_callbacks)
        return updates

    async def _run_through_callbacks(self, updates: ty.List[Event]) -> None:
        callback_await_coros = []
        for update in updates:
            callback_coros = [
                func(update) for func in self._new_event_callbacks
            ]
            wait_callback_coro = asyncio.wait(callback_coros)
            callback_await_coros.append(wait_callback_coro)

        await asyncio.wait(callback_await_coros)

    async def _resolve_faileds(self, response: Event):
        """
        Обрабатывает LongPoll ошибки (faileds)
        """
        if response["failed"] == 1:
            self._lp_requests_settings.update(ts=response["ts"])
        elif response["failed"] in (2, 3):
            await self._setup()
        else:
            raise ValueError("Invalid longpoll version")

    def _update_baked_request(self) -> None:
        self._baked_request = self.session.get(
            self._server_url, params=self._lp_requests_settings
        )
        self._baked_request = asyncio.create_task(self._baked_request)

    def add_event_callback(self, func: Callback) -> Callback:
        self._new_event_callbacks.append(func)
        return func

    def remove_event_callback(self, func: Callback) -> Callback:
        self._new_event_callbacks.remove(func)
        return func

    def run(self):
        asyncio.run(self.async_run())

    async def async_run(self):
        async for events in self:
            pass