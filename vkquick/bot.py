from __future__ import annotations
import asyncio
import datetime
import os
import time
import typing as ty

import huepy

import vkquick.current
import vkquick.event_handling.event_handler
import vkquick.event_handling.command
import vkquick.signal_handling.signal_handler
import vkquick.events_generators.event
import vkquick.event_handling.handling_info_scheme
import vkquick.exceptions
import vkquick.utils
import vkquick.debugger


class Bot:

    events_generator = vkquick.current.fetch("events_generator", "cb", "lp")

    def __init__(
        self,
        *,
        signal_handlers: ty.Optional[
            ty.Collection[
                vkquick.signal_handling.signal_handler.SignalHandler
            ]
        ] = None,
        event_handlers: ty.Optional[
            ty.Collection[vkquick.event_handling.event_handler.EventHandler]
        ] = None,
        debug_filter: ty.Optional[
            ty.Callable[[vkquick.events_generators.event.Event], bool]
        ] = None,
        debugger: ty.Optional[ty.Type[vkquick.debugger.Debugger]] = None,
        observing_path: str = ".",
    ):
        self.signal_handlers = signal_handlers or []
        self.event_handlers = event_handlers or []
        self.debug_filter = debug_filter or self.default_debug_filter
        self.observing_path = observing_path
        self.debugger = debugger or vkquick.debugger.Debugger

        self.release = os.getenv("VKQUICK_RELEASE")

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
            vkquick.utils.clear_console()
            print(huepy.yellow("Bot was stopped\n"))
            print(self._fetch_statistic_message())
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
            event_handlers_runner = self.run_through_event_handlers_release
        else:
            event_handlers_runner = self.run_through_event_handlers

        await self.events_generator.setup()
        async for events in self.events_generator:
            for event in events:
                asyncio.create_task(event_handlers_runner(event))

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
        handling_info = await asyncio.gather(*tasks)
        self.show_debug_info(event, handling_info)
        self._update_statistic_info(handling_info)

    async def run_through_event_handlers_release(
        self, event: vkquick.events_generators.event.Event
    ) -> None:
        """
        Оптимизированная версия `run_through_event_handlers`:
        не отправляет информацию в дебаггер
        """
        tasks = [
            asyncio.create_task(event_handler.handle_event(event))
            for event_handler in self.event_handlers
        ]
        handling_info = await asyncio.gather(*tasks)
        self._update_statistic_info(handling_info)

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

    async def call_signal(self, signal_name: str, *args, **kwargs) -> ty.Any:
        """
        Вызывает сигнал с именем `signal_name` и передает
        соответствующие аргументы. Если обработчика сигнала с
        таким именем нет, поднимется ошибка `NameError`
        """
        for signal_handler in self.signal_handlers:
            if signal_handler.signal_name == signal_name:
                return await vkquick.utils.sync_async_run(
                    signal_handler.reaction(*args, **kwargs)
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
            if info["are_filters_passed"] and isinstance(
                info["handler"], vkquick.event_handling.command.Command
            ):
                self._command_calls_count += 1

    @staticmethod
    def default_debug_filter(
        event: vkquick.events_generators.event.Event,
    ) -> bool:
        """
        Фильтр на событие для дебаггера по умолчанию
        """
        if event.type in ("message_new", "message_edit"):
            return True
