"""
Этот модуль предоставляет все возможности
по запуску бота
"""
from __future__ import annotations
import asyncio
import os
import traceback
import functools
import typing as ty

import vkquick.api
import vkquick.base.debugger
import vkquick.events_generators.longpoll
import vkquick.current
import vkquick.event_handling.event_handler
import vkquick.signal
import vkquick.events_generators.event
import vkquick.event_handling.handling_info_scheme
import vkquick.exceptions
import vkquick.utils
import vkquick.debuggers
from vkquick.events_generators.event import Event
from vkquick.command import Command


class _HandlerMarker:
    """
    Маркер хендлеров для бота. Позволяет помечать
    хендлер как обработчик событий или же как обработчик
    сигналов

        import vkquick as vq


        bot = vq.Bot.init_via_token("your-token")


        @bot.mark.event_handler
        @vq.Command(names=["hi"])
        def hi():
            return "hello!"


        @bot.mark.signal_handler
        @vq.SignalHandler(vq.ReservedSignal.STARTUP)
        def startup():
            print("Bot starts listening...")


        # В боте будет одна команда и один обработчик сигнала
        bot.run()

    Маркер нужно располагать над всеми декораторами
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    def command(self, command: Command) -> Command:
        """
        Маркер для обработчика событий
        """
        self.bot.commands.append(command)
        return command

    def signal_handler(
        self, handler: vkquick.signal.SignalHandler
    ) -> vkquick.signal.SignalHandler:
        """
        Маркер для обработчика сигналов
        """
        self.bot.signal_handlers.append(handler)
        return handler


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
        bot.event_handlers.append(hi)
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

    events_generator = vkquick.current.fetch("events_generator", "cb", "lp")

    def __init__(
        self,
        *,
        signal_handlers: ty.Optional[
            ty.Collection[vkquick.signal.SignalHandler]
        ] = None,
        commands: ty.Optional[ty.Collection[Command]] = None,
        debug_filter: ty.Optional[ty.Callable[[Event], bool]] = None,
        debugger: ty.Optional[
            ty.Type[vkquick.debuggers.ColoredDebugger]
        ] = None,
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
        self.signal_handlers = signal_handlers or []
        self.commands = commands or []
        self.debug_filter = debug_filter or self.default_debug_filter
        self.debugger = debugger or vkquick.debuggers.ColoredDebugger
        self.call_signal = vkquick.signal.SignalCaller(self.signal_handlers)

        self.event_waiters: ty.List[asyncio.Future] = []
        self.mark = _HandlerMarker(self)

    @classmethod
    def init_via_token(cls, token: str) -> Bot:
        """
        Создает все необходимое для запуска бота (current-объекты),
        используя только токен

        Не забудьте передать все необходимые обработчики событий
        и сигналов! Этот метод их не добавляет
        """
        # Создание необходимых объектов по информации с токена
        # и добавление их в куррент для использования с любой точки кода
        api = vkquick.api.API(token)
        vkquick.current.curs.api = api
        if api.token_owner == vkquick.api.TokenOwner.GROUP:
            vkquick.current.curs.lp = (
                vkquick.events_generators.longpoll.GroupLongPoll()
            )
        else:
            vkquick.current.curs.lp = (
                vkquick.events_generators.longpoll.UserLongPoll()
            )

        # Сам инстанс бота
        self = object.__new__(cls)
        self.__init__()
        return self

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

    def run(self) -> ty.NoReturn:
        """
        Запуск бота. Вызывает зарезервированный сигнал `STARTUP`
        пере запуском генератора по получению событий с их
        последующей обработкой. При любом завершении (намеренном или нет)
        вызывает зарезервированный сигнал `SHUTDOWN`. С флагом релиза
        бот будет перезагружаться при любых ошибках, т.е. он не упадет.
        """
        asyncio.run(self.async_run())

    async def async_run(self) -> ty.NoReturn:
        """
        Делает все то же самое, что `run`, только
        этот метод корутинный и его можно вызвать
        с другой корутиной конкурентно
        """
        self.call_signal.signal_name = vkquick.signal.ReservedSignal.STARTUP
        await vkquick.utils.sync_async_run(self.call_signal())
        await self.listen_events()
        # Сигнал для обозначения окончания работы бота
        self.call_signal.signal_name = vkquick.signal.ReservedSignal.SHUTDOWN
        await vkquick.utils.sync_async_run(self.call_signal())

    async def listen_events(self) -> ty.NoReturn:
        """
        Получает события с помощью одного из генераторов событий.
        После получение вызывает метод по обработке события
        на каждый `EventHandler` (или `Command`). Выбор метода
        зависит от флага релиза
        """
        if self.release:
            self.show_debug_info = self.show_debug_message_for_release

        await self.events_generator.setup()
        async for events in self.events_generator:
            for event in events:
                if event.type in ("message_new", 4):
                    asyncio.create_task(
                        self.pass_event_trough_commands(event)
                    )
                if event.from_group:
                    signal_calling = self.call_signal.via_name(
                        f"on_{event.type}", event
                    )
                    asyncio.create_task(
                        vkquick.utils.sync_async_run(signal_calling)
                    )

    async def pass_event_trough_commands(self, event: Event) -> None:
        """
        Конкурентно запускает процесс по обработке события
        на каждый `EventHandler`. После обработки выводит
        информацию в дебаггере, либо же, если флаг релиза,
        показывает только пойманные исключения
        """
        tasks = [
            asyncio.create_task(command.handle_event(event))
            for command in self.commands
        ]
        try:
            handling_info = await asyncio.gather(*tasks)
        except Exception:
            traceback.print_exc()
        else:
            self.show_debug_info(event, handling_info)
            await self._call_post_event_handling_signal(event, handling_info)

    def _set_new_event(
        self, event: vkquick.events_generators.event.Event
    ) -> None:
        """
        Выдает всем вейтерам событие
        """
        for waiter in self.event_waiters:
            waiter.set_result(event)

    async def fetch_new_event(self) -> vkquick.events_generators.event.Event:
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
        self.event_waiters.append(waiter)
        new_event = await waiter
        self.event_waiters.remove(waiter)
        return new_event

    def show_debug_info(
        self,
        event: vkquick.events_generators.event.Event,
        handling_info: ty.List[vkquick.base.debugger.HandlingStatus],
    ) -> None:
        """
        Показывает информацию в дебаггере. Если событие прошло фильтр,
        сначала выводит само событие, потом очищает окно терминала,
        а затем выводит сообщение, собранное дебаггером
        """
        if self.debug_filter(event):
            debugger = self.debugger(event, handling_info)
            debug_message = debugger.render()
            print(event.pretty_view())
            vkquick.utils.clear_console()
            print(debug_message)

    async def _call_post_event_handling_signal(
        self,
        event: vkquick.events_generators.event.Event,
        handling_info: vkquick.base.debugger.HandlingStatus,
    ) -> None:
        """
        Вызывает зарезервированный сигнал `POST_EVENT_HANDLING`.
        Вынесено в метод, чтобы избежать повторов
        """
        await vkquick.utils.sync_async_run(
            self.call_signal.via_name(
                vkquick.signal.ReservedSignal.POST_EVENT_HANDLING,
                event,
                handling_info,
            )
        )

    @staticmethod
    def default_debug_filter(
        event: vkquick.events_generators.event.Event,
    ) -> bool:
        """
        Фильтр на событие для дебаггера по умолчанию --
        Проверка на отправленное сообщение, либо редактирование.
        Редактирование для пользователей не добавлено, т.к.
        команды не адаптированны под обработку редактирования
        в User LP
        """
        return event.type in ("message_new", "message_edit", 4)

    @staticmethod
    def show_debug_message_for_release(
        _, handling_info: ty.List[vkquick.base.debugger.HandlingStatus],
    ) -> None:
        """
        Плейсхолдер для `show_debug_message` в момент
        запуска с флагом релиза
        """
        for scheme in handling_info:
            if scheme.exception_text:
                print(scheme.exception_text)
