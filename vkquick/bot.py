"""
Этот модуль предоставляет все возможности
по запуску бота
"""
from __future__ import annotations

import asyncio
import dataclasses
import inspect
import os
import re
import traceback
import typing as ty

from loguru import logger

from vkquick.api import API, TokenOwner
from vkquick.base.debugger import Debugger
from vkquick.base.filter import Filter
from vkquick.base.handling_status import HandlingStatus
from vkquick.command import Command
from vkquick.context import Context
from vkquick.events_generators.event import Event
from vkquick.events_generators.longpoll import (
    GroupLongPoll,
    LongPollBase,
    UserLongPoll,
)
from vkquick.signal import EventHandler, SignalHandler
from vkquick.utils import (
    clear_console,
    pretty_view,
    sync_async_callable,
    sync_async_run,
    mark_positional_only,
    cached_property,
)
from vkquick.wrappers.message import Message


@dataclasses.dataclass
class _Waiter:
    waiter: asyncio.Event = dataclasses.field(default_factory=asyncio.Event)
    new_events: ty.List[Event] = dataclasses.field(default_factory=list)


class Bot:
    """
    Этот класс оборудует действиями с получением событий
    от вк, а затем запускает процесс обработки этого события
    с последующим информированием: что случилось, как прошла
    обработка (если включен режим дебага). Помимо обычной обработки,
    можно получать новые события и обрабатывать в любой точке кода,
    т.е. `Bot` -- центр управления всем, что должно происходить в боте.
    """

    def __init__(
        self,
        *,
        api: API,
        events_generator: LongPollBase,
        signal_handlers: ty.Optional[ty.Collection[SignalHandler]] = None,
        commands: ty.Optional[ty.Collection[Command]] = None,
        event_handlers: ty.Optional[ty.Collection[EventHandler]] = None,
        debug_filter: ty.Optional[ty.Callable[[Event], bool]] = None,
        debugger: ty.Optional[ty.Type[Debugger]] = None,
        log_path: str = "vkquick.log"
    ):
        """
        * `commands`: Список обрабатываемых команд
        * `signal_handlers`: Список доступных обработчиков сигналов
        * `debug_filter`: Фильтр на событие, возвращающий `True`/`False`. Необходим
        для того, чтобы лишние события не засоряли дебаггер. Если вернулось `False`,
        информации в дебаггере не будет
        * `debugger`: Дебаггер, собирающий по событию и информации по обработке
        события сообщение  для наглядного отображения произошедшего
        """
        self._signal_handlers = signal_handlers or []
        self._commands = commands or []
        self._event_handlers = event_handlers or []
        self._debug_filter = debug_filter or self.default_debug_filter
        self._debugger = debugger
        self._api = api
        self._events_generator = events_generator
        self._log_path = log_path

        self._event_waiters: ty.List[_Waiter] = []

    @property
    def commands(self) -> ty.List[Command]:
        return self._commands

    @property
    def api(self) -> API:
        return self._api

    @property
    def events_generator(self) -> LongPollBase:
        return self._events_generator

    @classmethod
    @mark_positional_only("token")
    def init_via_token(
        cls,
        token: str,
        *,
        signal_handlers: ty.Optional[ty.Collection[SignalHandler]] = None,
        commands: ty.Optional[ty.Collection[Command]] = None,
        event_handlers: ty.Optional[ty.Collection[EventHandler]] = None,
        debug_filter: ty.Optional[ty.Callable[[Event], bool]] = None,
        debugger: ty.Optional[ty.Type[Debugger]] = None,
    ) -> Bot:
        """
        Создает все необходимое для запуска бота (current-объекты),
        используя только токен
        """
        api = API(token)
        if api.token_owner == TokenOwner.GROUP:
            lp = GroupLongPoll(api)
        else:
            lp = UserLongPoll(api)

        return cls(
            api=api,
            events_generator=lp,
            signal_handlers=signal_handlers,
            commands=commands,
            event_handlers=event_handlers,
            debugger=debugger,
            debug_filter=debug_filter,
        )

    @mark_positional_only("handler")
    def add_command(
        self,
        handler: ty.Optional[
            sync_async_callable(..., ty.Optional[str])
        ] = None,
        *,
        prefixes: ty.Iterable[str] = (),
        names: ty.Iterable[str] = (),
        argline: ty.Optional[str] = None,
        title: ty.Optional[str] = None,
        description: ty.Optional[str] = None,
        routing_command_re_flags: re.RegexFlag = re.IGNORECASE,
        on_invalid_argument: ty.Optional[
            ty.Dict[str, ty.Union[sync_async_callable([Context], ...), str]]
        ] = None,
        on_invalid_filter: ty.Optional[
            ty.Dict[
                ty.Type[Filter],
                ty.Union[sync_async_callable([Context], ...), str],
            ]
        ] = None,
        extra: ty.Optional[dict] = None,
        run_in_thread: bool = False,
        run_in_process: bool = False,
        use_regex_escape: bool = True,
        any_text: bool = False,
        payload_names: ty.Collection[str] = (),
    ) -> Command:
        if handler is None or isinstance(handler, (set, list, str, tuple)):
            if isinstance(handler, (set, list, str, tuple)):
                names = handler
            command_params = locals().copy()
            del command_params["handler"]
            del command_params["self"]
            command = Command(**command_params)
        else:
            if not isinstance(handler, Command):
                raise TypeError(
                    f"Added command should be `Command` "
                    f"instance (built via `add_command` "
                    f"or `Command` class), "
                    f"got `{type(handler)}`"
                )
            command = handler
        self._commands.append(command)
        return command

    @mark_positional_only("handler")
    def add_signal_handler(
        self,
        handler: ty.Optional[sync_async_callable(..., ty.Any)] = None,
        extra_names: ty.Optional[ty.List[str]] = None,
        all_names: ty.Optional[ty.List[str]] = None,
    ) -> SignalHandler:
        if isinstance(handler, SignalHandler):
            signal_handler = handler
        else:
            signal_handler = SignalHandler(  # noqa
                handler, extra_names=extra_names, all_names=all_names
            )
        self._signal_handlers.append(signal_handler)
        return signal_handler

    @mark_positional_only("handler")
    def add_event_handler(
        self,
        handler: ty.Optional[sync_async_callable(..., ty.Any)] = None,
        extra_types: ty.Optional[ty.List[str]] = None,
        all_types: ty.Optional[ty.List[str]] = None,
    ) -> EventHandler:
        if isinstance(handler, SignalHandler):
            event_handler = handler
        else:
            event_handler = EventHandler(  # noqa
                handler, extra_types=extra_types, all_types=all_types
            )
        self._event_handlers.append(event_handler)
        return event_handler

    def run(self) -> ty.NoReturn:
        """
        Запуск бота. Вызывает зарезервированный сигнал `STARTUP`
        пере запуском генератора по получению событий с их
        последующей обработкой. При любом завершении (намеренном или нет)
        вызывает зарезервированный сигнал `SHUTDOWN`. С флагом релиза
        бот будет перезагружаться при любых ошибках, т.е. он не упадет.
        """
        logger.add(self._log_path)
        try:
            asyncio.run(self.async_run())
        except KeyboardInterrupt:
            pass

    async def async_run(self) -> ty.NoReturn:
        """
        Делает все то же самое, что `run`, только
        этот метод корутинный и его можно вызвать
        с другой корутиной конкурентно
        """
        try:
            await sync_async_run(
                self.call_signal("startup", self)
            )
            logger.info("Run events listening")
            await self.listen_events()
        finally:
            logger.info("End events listening")
            # Сигнал для обозначения окончания работы бота
            await sync_async_run(
                self.call_signal("shutdown", self)
            )
            await self.events_generator.close_session()

    async def listen_events(self) -> ty.NoReturn:
        """
        Получает события с помощью одного из генераторов событий.
        После получение вызывает метод по обработке события
        на каждый `EventHandler` (или `Command`). Выбор метода
        зависит от флага релиза
        """

        async for events in self.events_generator:
            self._set_new_events(events)
            for event in events:
                asyncio.create_task(self.route_event_purpose(event))

    async def route_event_purpose(self, event: Event):
        if event.type in ("message_new", "message_reply"):
            asyncio.create_task(self.pass_event_trough_commands(event))
        elif event.type == 4:
            asyncio.create_task(self._run_commands_via_user_lp_message(event))
        for event_handler in self._event_handlers:
            if event_handler.is_handling_name(event.type):
                asyncio.create_task(sync_async_run(event_handler.call(event)))

    async def _run_commands_via_user_lp_message(self, event: Event):
        try:
            await self.extend_userlp_message(event)
        except Exception:
            traceback.print_exc()
            print(repr(event))
            print(
                "It's OK, bot is still working, but if you see it, report, please"
            )
        else:
            await self.pass_event_trough_commands(event)

    async def extend_userlp_message(self, event: Event):
        extended_message = await self._shared_box.api.messages.get_by_id(
            allow_cache_=True, message_ids=event[1]
        )
        extended_message = extended_message.items[0]
        event.set_message(extended_message)

    async def pass_event_trough_commands(self, event: Event) -> None:
        """
        Конкурентно запускает процесс по обработке события
        на каждый `EventHandler`. После обработки выводит
        информацию в дебаггере, либо же, если флаг релиза,
        показывает только пойманные исключения
        """
        tasks = [
            asyncio.create_task(command.handle_event(event, self))
            for command in self.commands
        ]
        handling_info = await asyncio.gather(*tasks)
        await sync_async_run(
            self.call_signal("post_event_handling", event, handling_info)
        )

    def _set_new_events(self, events: ty.List[Event]) -> None:
        """
        Выдает всем вейтерам событие
        """
        for waiter in self._event_waiters:
            waiter.new_events.append(events)
            waiter.waiter.set()

    async def run_sublistening(self) -> ty.Generator[Event, None, None]:
        waiter = _Waiter()
        self._event_waiters.append(waiter)
        try:
            while True:
                await waiter.waiter.wait()
                pack = waiter.new_events.pop(0)
                for new_event in pack:
                    yield new_event
                waiter.waiter.clear()

        finally:
            self._event_waiters.remove(waiter)

    async def show_debug_info(
        self, event: Event, handling_info: ty.List[HandlingStatus],
    ) -> None:
        """
        Показывает информацию в дебаггере. Если событие прошло фильтр,
        сначала выводит само событие, потом очищает окно терминала,
        а затем выводит сообщение, собранное дебаггером
        """
        if self._debug_filter(event):
            sender_name = await self._get_sender_name(event.msg)
            debugger = self._debugger(
                sender_name=sender_name,
                message_text=event.msg.text,
                schemes=handling_info,
            )
            debug_message = debugger.render()
            print(pretty_view(event.msg.fields))
            clear_console()
            print(debug_message)

    async def _get_sender_name(self, message: Message):
        if message.from_id > 0:
            sender = await self.shared_box.api.fetch_user_via_id(
                message.from_id
            )
            sender = format(sender, "<fn> <ln>")
        else:
            sender = await self.shared_box.api.groups.get_by_id(
                allow_cache_=True, group_id=abs(message.from_id)
            )
            sender = sender[0].name

        return sender

    def call_signal(self, name: str, *args, **kwargs) -> ty.Any:
        for handler in self._signal_handlers:
            if handler.is_handling_name(name):
                logger.debug(f"Call signal with name: `{name}`, args: {args}, kwargs: {kwargs}")
                return handler.call(*args, **kwargs)

    def copy(self, new_token: str) -> Bot:
        api = API(new_token)
        if api.token_owner == TokenOwner.GROUP:
            lp = GroupLongPoll(api)
        else:
            lp = UserLongPoll(api)

        new_bot = self.__class__(
            api=api,
            events_generator=lp,
            signal_handlers=self._signal_handlers,
            commands=self._commands,
            event_handlers=self._event_handlers,
            debug_filter=self._debug_filter,
            debugger=self._debugger,
        )
        return new_bot

    def make_many_copies(self, tokens: ty.Iterable[str]) -> ty.List[Bot]:
        multiplied_bots = [self]
        for token in tokens:
            new_bot = self.copy(token)
            multiplied_bots.append(new_bot)
        return multiplied_bots

    @staticmethod
    def default_debug_filter(event: Event,) -> bool:
        """
        Фильтр на событие для дебаггера по умолчанию --
        Проверка на отправленное сообщение, либо редактирование.
        Редактирование для пользователей не добавлено, т.к.
        команды не адаптированны под обработку редактирования
        в User LP
        """
        return event.type in ("message_new", "message_reply", 4)

async def async_run_many_bots(bots: ty.List[Bot]) -> ty.NoReturn:
    os.environ["VKQUICK_RELEASE"] = "1"
    run_tasks = [bot.async_run() for bot in bots]
    await asyncio.wait(run_tasks)


def run_many_bots(bots: ty.List[Bot]) -> ty.NoReturn:
    asyncio.run(async_run_many_bots(bots))
