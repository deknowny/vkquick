"""
Этот модуль предоставляет все возможности
по запуску бота
"""
from __future__ import annotations
import asyncio
import inspect
import os
import traceback
import functools
import re
import typing as ty

from vkquick.api import API, TokenOwner
from vkquick.base.debugger import Debugger
from vkquick.base.handling_status import HandlingStatus
from vkquick.events_generators.longpoll import (
    GroupLongPoll,
    UserLongPoll,
    LongPollBase,
)
from vkquick.shared_box import SharedBox
from vkquick.signal import SignalHandler, EventHandler
from vkquick.events_generators.event import Event
from vkquick.utils import (
    sync_async_run,
    clear_console,
    pretty_view,
    sync_async_callable,
)
from vkquick.debuggers import ColoredDebugger
from vkquick.command import Command
from vkquick.base.filter import Filter
from vkquick.context import Context


class Bot:
    """
    Этот класс оборудует действиями с получением событий
    от вк, а затем запускает процесс обработки этого события
    с последующим информированием: что случилось, как прошла
    обработка (если включен режим дебага). Помимо обычной обработки,
    можно получать новые события и обрабатывать в любой точке кода,
    т.е. `Bot` -- центр управления всем, что должно происходить в боте.

    Пример бота, отвечающего `hello!` на сообщение с `hi`


        import vkquick as vq


        # Самая обычная команда, которая отвечает `hello!`
        @vq.Command(names=["hi"])
        def hi():
            return "hello!"


        bot = vq.Bot.init_via_token("your-token")
        bot.commands.append(hi)
        bot.run()


    Это автоматически создаст все необходимые current-объекты (API, LongPoll).
    Если вы хотите более детально настроить их, можете выставить их вручную:


        import vkquick as vq


        @vq.Command(names=["hi"])
        def hi():
            return "hello!"


        # Можете дать свои параметры в эти объекты
        vq.curs.api = vq.API("your-token")
        vq.curs.lp = vq.GroupLongPoll()  # Или UserLongPoll

        bot = vq.Bot(event_handlers=[hi])
        bot.run()


    Вместо добавления хендлеров в объект бота вручную, можно
    использовать маркеры (пример есть в классе выше)
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
    ):
        """
        * `commands`: Список обрабатываемых команд
        * `signal_handlers`: Список доступных обработчиков сигналов
        * `debug_filter`: Фильтр на событие, возвращающий `True`/`False`. Необходим
        для того, чтобы лишние события не засоряли дебаггер. Если вернулось `False`,
        информации в дебаггере не будет
        * `debugger`: Дебаггер, собирающий по событию и информации по обработке
        события сообщение в терминал для наглядного отображения произошедшего
        """
        self._signal_handlers = signal_handlers or []
        self._commands = commands or []
        self._event_handlers = event_handlers or []
        self._debug_filter = debug_filter or self.default_debug_filter
        self._debugger = debugger or ColoredDebugger

        self._event_waiters: ty.List[asyncio.Future] = []

        self._shared_box = SharedBox(
            api=api, events_generator=events_generator, bot=self
        )

    @property
    def commands(self) -> ty.List[Command]:
        return self._commands

    @property
    def api(self) -> API:
        return self._shared_box.api

    @property
    def events_generator(self) -> LongPollBase:
        return self._shared_box.events_generator

    @property
    def shared_box(self) -> SharedBox:
        return self._shared_box

    @classmethod
    def init_via_token(cls, token: str) -> Bot:
        """
        Создает все необходимое для запуска бота (current-объекты),
        используя только токен

        Не забудьте передать все необходимые обработчики событий
        и сигналов! Этот метод их не добавляет
        """
        api = API(token)
        if api.token_owner == TokenOwner.GROUP:
            lp = GroupLongPoll(api)
        else:
            lp = UserLongPoll(api)

        return cls(api=api, events_generator=lp)

    @functools.cached_property
    def release(self) -> bool:
        """
        Флаг, означающий, что бот запущен на продакшене.
        Используется в моментах, в которых можно сделать оптимизации.
        Например, выключение дебаггера. Вы также можете строить
        логику у себя, основываясь на этом флаге
        """
        release = os.getenv("VKQUICK_RELEASE")
        if release is not None and release.isdigit():
            release = int(release)
        release = bool(release)
        return release

    def add_command(
        self,
        handler: ty.Optional[
            sync_async_callable(..., ty.Optional[str])
        ] = None,
        /,
        *,
        prefixes: ty.Iterable[str] = (),
        names: ty.Iterable[str] = (),
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
    ) -> Command:
        if handler is None:
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

    def add_signal_handler(
        self,
        handler: ty.Optional[sync_async_callable(..., ty.Any)] = None,
        /,
        extra_names: ty.Optional[ty.List[str]] = None,
        all_names: ty.Optional[ty.List[str]] = None,
    ) -> SignalHandler:
        signal_handler = SignalHandler(  # noqa
            handler, extra_names=extra_names, all_names=all_names
        )
        self._signal_handlers.append(signal_handler)
        return signal_handler

    def add_event_handler(
        self,
        handler: ty.Optional[sync_async_callable(..., ty.Any)] = None,
        /,
        extra_types: ty.Optional[ty.List[str]] = None,
        all_types: ty.Optional[ty.List[str]] = None,
    ) -> EventHandler:
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
                self._call_signal_with_optional_shared_box("startup")
            )
            await self.listen_events()
        finally:
            # Сигнал для обозначения окончания работы бота
            await sync_async_run(
                self._call_signal_with_optional_shared_box("shutdown")
            )
            await self._shared_box.events_generator.close_session()

    async def listen_events(self) -> ty.NoReturn:
        """
        Получает события с помощью одного из генераторов событий.
        После получение вызывает метод по обработке события
        на каждый `EventHandler` (или `Command`). Выбор метода
        зависит от флага релиза
        """
        await self._shared_box.events_generator.setup()
        async for events in self._shared_box.events_generator:
            for event in events:
                if event.type in ("message_new", "message_reply"):
                    asyncio.create_task(
                        self.pass_event_trough_commands(event)
                    )
                elif event.type == 4:
                    # TODO: optimize (#34)
                    extended_message = await self._shared_box.api.messages.get_by_id(
                        allow_cache_=True, message_ids=event[1]
                    )
                    extended_message = extended_message.items[0]
                    event.set_message(extended_message)
                    asyncio.create_task(
                        self.pass_event_trough_commands(event)
                    )
                for event_handler in self._event_handlers:
                    if event_handler.is_handling_name(event.type):
                        asyncio.create_task(
                            sync_async_run(event_handler.call(event))
                        )

    async def pass_event_trough_commands(self, event: Event) -> None:
        """
        Конкурентно запускает процесс по обработке события
        на каждый `EventHandler`. После обработки выводит
        информацию в дебаггере, либо же, если флаг релиза,
        показывает только пойманные исключения
        """
        tasks = [
            asyncio.create_task(command.handle_event(event, self._shared_box))
            for command in self.commands
        ]
        try:
            handling_info = await asyncio.gather(*tasks)
        except Exception:
            traceback.print_exc()
        else:
            if not self.release:
                await self.show_debug_info(event, handling_info)
            await self._call_post_event_handling_signal(event, handling_info)

    def _set_new_event(self, event: Event) -> None:
        """
        Выдает всем вейтерам событие
        """
        for waiter in self._event_waiters:
            waiter.set_result(event)

    async def fetch_new_event(self) -> Event:
        """
        Аналог `asyncio.Event.wait()`. Используйте внутри своей реакции,
        чтобы получить новое событие

            import vkquick as vq


            @vq.Command(names=["foo"])
            def foo():
                new_event = await vq.curs.bot.fetch_new_event()
                ...

        Так можно выстраивать цепочки общения с пользователем
        """
        waiter = asyncio.Future()
        self._event_waiters.append(waiter)
        new_event = await waiter
        self._event_waiters.remove(waiter)
        return new_event

    async def show_debug_info(
        self, event: Event, handling_info: ty.List[HandlingStatus],
    ) -> None:
        """
        Показывает информацию в дебаггере. Если событие прошло фильтр,
        сначала выводит само событие, потом очищает окно терминала,
        а затем выводит сообщение, собранное дебаггером
        """
        if self._debug_filter(event):
            debugger = self._debugger(self.api, event, handling_info)  # noqa
            debug_message = debugger.render()
            print(pretty_view(event.msg.fields))
            clear_console()
            print(debug_message)

    async def _call_post_event_handling_signal(
        self, event: Event, handling_info: HandlingStatus,
    ) -> None:
        """
        Вызывает зарезервированный сигнал `POST_EVENT_HANDLING`.
        Вынесено в метод, чтобы избежать повторов
        """
        await sync_async_run(
            self.call_signal("post_event_handling", event, handling_info)
        )

    def call_signal(self, name: str, *args, **kwargs) -> ty.Any:
        for handler in self._signal_handlers:
            if handler.is_handling_name(name):
                return handler.call(*args, **kwargs)

    def _call_signal_with_optional_shared_box(self, name: str):
        for handler in self._signal_handlers:
            if handler.is_handling_name(name):
                parameters = inspect.signature(handler.handler).parameters
                if len(parameters) == 1:
                    return handler.call(self.shared_box)
                elif len(parameters) == 0:
                    return handler.call()
                else:
                    raise TypeError(
                        f"Signal with name `{name}` should"
                        f"take only 1 or 0 arguments"
                    )

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

    @staticmethod
    def show_debug_message_for_release(
        _, handling_info: ty.List[HandlingStatus],
    ) -> None:
        """
        Плейсхолдер для `show_debug_message` в момент
        запуска с флагом релиза
        """
        for scheme in handling_info:
            if scheme.exception_text:
                print(scheme.exception_text)


async def async_run_many_bots(bots: ty.List[Bot]) -> ty.NoReturn:
    os.environ["VKQUICK_RELEASE"] = "1"
    run_tasks = [bot.async_run() for bot in bots]
    await asyncio.wait(run_tasks)


def run_many_bots(bots: ty.List[Bot]) -> ty.NoReturn:
    asyncio.run(async_run_many_bots(bots))
