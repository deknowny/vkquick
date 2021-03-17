from __future__ import annotations

import asyncio
import dataclasses
import typing as ty

from vkquick.api import API
from vkquick.bases.easy_decorator import easy_method_decorator
from vkquick.bases.event import Event
from vkquick.bases.events_factories import EventsFactory
from vkquick.event_handler.context import EventHandlingContext
from vkquick.event_handler.handler import EventHandler
from vkquick.longpoll import GroupLongPoll, UserLongPoll
from vkquick.signal import SignalHandler
from vkquick.sync_async import sync_async_callable, sync_async_run

if ty.TYPE_CHECKING:
    from vkquick import Filter
    from vkquick.bases.middleware import Middleware


@dataclasses.dataclass
class EventProcessingContext:
    """
    Контекстное хранилище, инициализируемое на
    каждое новое событие.
    """

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
        events_factory: ty.Optional[EventsFactory] = None,
        event_handlers: ty.Optional[ty.List[EventHandler]] = None,
        signals: ty.Optional[ty.Dict[str, SignalHandler]] = None,
        middlewares: ty.Optional[ty.List[Middleware]] = None,
    ):
        self._api = api
        self._events_factory = events_factory
        self._event_handlers = event_handlers or []
        self._signals = signals or {}
        self._middlewares = middlewares or []

    @classmethod
    def via_token(cls, token: str, **kwargs) -> Bot:
        """
        Позволяет создать инстанс бота через токен,
        автоматически создавая необходимый инстанс API.
        Универсален как для для пользователей, так и групп

        :param token: Токен пользователя/группы, от чьего лица будет работать бот
        :param kwargs: Настройки, которые можно передать при инициализации бота обычным способом

        :return: Новый объекта бота, готовый к добавлению обработчиков и запуску
        """
        api = API(token)
        return cls(api=api, **kwargs)

    @property
    def api(self) -> API:
        return self._api

    @property
    def events_factory(self) -> EventsFactory:
        """
        Текущая фабрика событий, используемая для получения новых событий.
        """
        return self._events_factory

    @property
    def event_handlers(self) -> ty.List[EventHandler]:
        """
        Текущий список обработчиков событий.
        """
        return self._event_handlers

    @property
    def signals(self) -> ty.Dict[str, SignalHandler]:
        """
        Текущий словарь обработчиков сигналов.
        """
        return self._signals

    @property
    def middlewares(self) -> ty.List[Middleware]:
        """
        Текущий список используемых мидлваров.
        """
        return self._middlewares

    def run(self) -> ty.NoReturn:
        """
        Запускает работу бота, т.е. запускает логику
        по получению новых событий с последующей необходимой
        обработкой мидлварами, хендлерами сигналов и событий.

        Перед началом запуска логики с получением событий, вызывается
        сигнал `startup`. После завершения работы вызовется сигнал `shutdown`.
        Каждый из сигналов принимает инстанс бота в качестве аргумента.

        Бот работает асинхронно, не смотря на синхронный запуск.

        :return: Запуск вечный, этот метод не возвращает никакое значение.
        """
        asyncio.run(self.coroutine_run())

    async def coroutine_run(self) -> ty.NoReturn:
        """
        Аналогичная методу `run` метод, только являющийся
        корутиной и позволяющий запустить бота конкурентно с
        другими корутинами

        :return: Запуск вечный, этот метод не возвращает никакое значение.
        """
        try:
            await self._setup_events_factory()
            startup_signal = self._signals.get("startup")
            if startup_signal is not None:
                await sync_async_run(startup_signal(self))
            async with self._events_factory:
                await self.run_listening_events()
        finally:
            shutdown_signal = self._signals.get("shutdown")
            if shutdown_signal is not None:
                await sync_async_run(shutdown_signal(self))

    async def run_listening_events(self) -> ty.NoReturn:
        """
        Метод, конкретно отвечающий за получение событий,
        инициализации соответствующего с ним контекста и запуска
        обработки этого контекста

        :return: Запуск вечный, этот метод не возвращает никакое значение.
        """
        async for event in self._events_factory.listen():
            epctx = EventProcessingContext(bot=self, event=event)
            asyncio.create_task(self._route_context(epctx))

    async def _setup_events_factory(self) -> None:
        """
        Если при инициализации не была указана фабрика событий,
        то в зависимости от типа владельца токена фабрикой будет
        либо лп группы, либо лп пользователя
        """
        if self._events_factory is None:
            owner = await self._api.fetch_token_owner_entity()
            if owner.is_group:
                self._events_factory = GroupLongPoll(self._api)
            else:
                self._events_factory = UserLongPoll(self._api)

    async def _route_context(self, epctx: EventProcessingContext) -> None:
        """
        Направляет контекст с событием в необходимые точки:
        через мидлвары и обработчики событий.

        :param epctx: Контекст обработки события.
        """
        await self._call_forward_middlewares(epctx)
        await self._pass_context_through_handlers(epctx)
        await self._call_afterword_middlewares(epctx)

    async def _pass_context_through_handlers(
        self, epctx: EventProcessingContext
    ) -> None:
        """
        Конкурентно передает контекст события по всем хендлерам событий.
        Контексты хэндлеров с состоянием их обрабротки добавляются
        в контекст события, т.е. их можно получить из мидлваров.

        :param epctx: Контекст обработки события.
        """
        handling_coros = []
        for handler in self._event_handlers:
            ehctx = EventHandlingContext(epctx=epctx)
            epctx.event_handling_contexts.append(ehctx)
            handling_coros.append(handler(ehctx=ehctx))
        await asyncio.gather(*handling_coros)

    async def _call_forward_middlewares(
        self, epctx: EventProcessingContext
    ) -> None:
        """
        Вызывает мидлвары перед обработкой события хэндлерами событий

        :param epctx: Контекст обработки события
        """
        for middleware in self._middlewares:
            await sync_async_run(middleware.foreword(epctx))

    async def _call_afterword_middlewares(
        self, epctx: EventProcessingContext
    ) -> None:
        """
        Вызывает мидлвары после обработки события хэндлерами событий

        :param epctx: Контекст обработки события
        """
        for middleware in reversed(self._middlewares):
            await sync_async_run(middleware.afterword(epctx))

    @easy_method_decorator
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
    ) -> EventHandler:
        """
        Добавляет обработчик события в бота.

        Если `__handler` уже является инстансом `EventHandler`,
        то обработчик просто добавится в бота. Иначе будет создан
        новый объект обработчика с другими полями этого метода
        и уже он будет добавлен.


        :param __handler: Обработчик события/функция, которая
            будет передана при создании обработчика
        :param handling_event_types: Множество типов обрабатываемых событий
        :param filters: Фильтры обработчика событий
        :param post_handling_callbacks: Функция, вызываемая после вызова фильтров и реакции
        :param pass_ehctx_as_argument: Нужно ли передавать контекст в качестве аргумента
        :return: Объект обработчика событий
        """
        if not isinstance(__handler, EventHandler):
            __handler = EventHandler(
                __handler,
                handling_event_types=handling_event_types,
                filters=filters,
                post_handling_callbacks=post_handling_callbacks,
                pass_ehctx_as_argument=pass_ehctx_as_argument,
            )

        self._event_handlers.append(__handler)
        return __handler

    @easy_method_decorator
    def add_signal_handler(
        self,
        __handler: ty.Optional[ty.Callable] = None,
        *,
        name: ty.Optional[str] = None,
    ):
        if not isinstance(__handler, SignalHandler):
            __handler = SignalHandler(__handler, name=name)
        self._signals[__handler.name] = __handler
        return __handler

    @easy_method_decorator
    def add_middleware(self, __handler: ty.Optional[Middleware] = None):
        self._middlewares.append(__handler)
