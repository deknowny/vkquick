from __future__ import annotations
import asyncio
import datetime
import os
import time
import traceback
import typing as ty

import huepy

import vkquick.current
import vkquick.event_handling.event_handler
import vkquick.event_handling.command
import vkquick.signal
import vkquick.events_generators.event
import vkquick.event_handling.handling_info_scheme
import vkquick.exceptions
import vkquick.utils
import vkquick.debuggers


class Bot:

    events_generator = vkquick.current.fetch("events_generator", "cb", "lp")

    def __init__(
        self,
        *,
        signal_handlers: ty.Optional[
            ty.Collection[vkquick.signal.SignalHandler]
        ] = None,
        event_handlers: ty.Optional[
            ty.Collection[vkquick.event_handling.event_handler.EventHandler]
        ] = None,
        debug_filter: ty.Optional[
            ty.Callable[[vkquick.events_generators.event.Event], bool]
        ] = None,
        debugger: ty.Optional[
            ty.Type[vkquick.debuggers.ColoredDebugger]
        ] = None,
    ):
        self.signal_handlers = signal_handlers or []
        self.event_handlers = event_handlers or []
        self.debug_filter = debug_filter or self.default_debug_filter
        self.debugger = debugger or vkquick.debuggers.ColoredDebugger
        self.call_signal = vkquick.signal.SignalCaller(self.signal_handlers)

        self.release = os.getenv("VKQUICK_RELEASE")
        if self.release is not None and self.release.isdigit():
            self.release = int(self.release)
        self.release = bool(self.release)

        self.event_waiters = []

        # Статистика
        self._start_time = time.time()
        self._handled_events_count = 0
        self._command_calls_count = 0

    def run(self):
        """
        Запуск бота. Вызывает сигнал `startup`,
        потом запускает процесс по получению и обработке событий.
        При завершении вызывает `shutdown`
        """
        asyncio.run(self.call_signal("startup"))
        try:
            asyncio.run(self.listen_events())
        except KeyboardInterrupt:
            if self.release:
                vkquick.utils.clear_console()
            print(huepy.yellow("Bot was stopped\n"))
            print(self._fetch_statistic_message())
        except Exception as exc:
            print(exc)
        finally:
            asyncio.run(self.call_signal("shutdown"))

    async def listen_events(self):
        """
        Получает события с помощью одного из генераторов событий.
        После получение вызывает метод по обработке события
        на каждый `EventHandler` (или `Command`). Выбор метода
        зависит от того, является ли запуск бота деплоем
        (переменная окружения `VKQUICK_RELEASE`)
        """
        if self.release:
            self.show_debug_info = self.show_debug_message_for_release

        await self.events_generator.setup()
        async for events in self.events_generator:
            for event in events:
                self.set_new_event(event)
                asyncio.create_task(self.run_through_event_handlers(event))

    async def run_through_event_handlers(
        self, event: vkquick.events_generators.event.Event
    ) -> None:
        """
        Конкурентно запускает процесс по обработке события
        на каждый `EventHandler`. После обработки выводит
        информацию в дебаггере
        """
        tasks = [
            asyncio.create_task(event_handler.handle_event(event))
            for event_handler in self.event_handlers
        ]
        try:
            handling_info = await asyncio.gather(*tasks)
        except Exception as exc:
            traceback.print_exc()
        else:
            self.show_debug_info(event, handling_info)
            self._update_statistic_info(handling_info)
            await self._call_post_event_handling_signal(event, handling_info)

    def set_new_event(
        self, event: vkquick.events_generators.event.Event
    ) -> None:
        """
        Выдает всем вейтерам событие
        """
        for waiter in self.event_waiters:
            waiter.set_result(event)

    async def fetch_new_event(self) -> vkquick.events_generators.event.Event:
        """
        Аналог `asyncio.Event.wait()`
        """
        waiter = asyncio.Future()
        self.event_waiters.append(waiter)
        new_event = await waiter
        self.event_waiters.remove(waiter)
        return new_event

    def show_debug_info(
        self,
        event: vkquick.events_generators.event.Event,
        handling_info: ty.List[
            vkquick.event_handling.handling_info_scheme.HandlingInfoScheme
        ],
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
        handling_info: vkquick.event_handling.handling_info_scheme.HandlingInfoScheme,
    ) -> None:
        self.call_signal.signal_name = (
            vkquick.signal.ReservedSignal.POST_EVENT_HANDLING
        )
        await vkquick.utils.sync_async_run(
            self.call_signal(event, handling_info)
        )

    def _fetch_statistic_message(self) -> str:
        """
        Собирает сообщение о статистике обработки
        """
        data: ty.Dict[str, str] = {}

        uptime = time.time() - self._start_time
        uptime = int(uptime)
        since = datetime.datetime.fromtimestamp(self._start_time)
        uptime = f"{uptime}s (since {since:%H:%M %d-%m-%Y})"

        data["Uptime"] = uptime
        data["Count of got events"] = str(self._handled_events_count)
        data["Command calls count"] = str(self._command_calls_count)

        info: ty.List[str] = []
        for key, value in data.items():
            key = huepy.blue(key)
            info.append(f"{key}: {value}")

        info: str = "\n".join(info)
        return info

    def _update_statistic_info(
        self,
        handling_info: ty.List[
            vkquick.event_handling.handling_info_scheme.HandlingInfoScheme
        ],
    ) -> None:
        """
        Обновляет информацию по статистике
        """
        self._handled_events_count += 1
        for info in handling_info:
            if info.all_filters_passed and isinstance(
                info.handler, vkquick.event_handling.command.Command
            ):
                self._command_calls_count += 1

    @staticmethod
    def default_debug_filter(
        event: vkquick.events_generators.event.Event,
    ) -> bool:
        """
        Фильтр на событие для дебаггера по умолчанию
        """
        return event.type in ("message_new", "message_edit", 4)

    @staticmethod
    def show_debug_message_for_release(_, handling_info):
        for scheme in handling_info:
            if scheme.exception_text:
                print(scheme.exception_text)
