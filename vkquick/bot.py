import asyncio
import datetime
import sys
import os
import typing as ty

import sty
import watchgod

import vkquick.current
import vkquick.event_handling.event_handler
import vkquick.signal_handling.signal_handler
import vkquick.events_generators.event
import vkquick.event_handling.handling_info_scheme
import vkquick.exceptions
import vkquick.utils


class Bot:

    events_generator = vkquick.current.fetch("events_generator", "cb", "lp")

    def __init__(
        self,
        *,
        signal_handlers: ty.Collection[
            vkquick.signal_handling.signal_handler.SignalHandler
        ],
        event_handlers: ty.Collection[
            vkquick.event_handling.event_handler.EventHandler
        ],
        debug_filter: ty.Optional[
            ty.Callable[[vkquick.events_generators.event.Event], bool]
        ] = None,
        observing_path: str = ".",
    ):
        self.signal_handlers = signal_handlers
        self.event_handlers = event_handlers
        self.debug_filter = debug_filter or self.default_debug_filter
        self.observing_path = observing_path
        self.reload_now = False

    def run(self):
        """
        Запуск бота. Вызывает сигнал `startup`,
        потом запускает процесс по получению и обработке событий,
        при завершении вызывает `shutdown`
        """
        asyncio.run(self.call_signal("startup"))
        try:
            asyncio.run(self._run())
        except vkquick.exceptions.BotReloadNow:
            pass
        except KeyboardInterrupt:
            print(sty.fg.yellow + "\nBot was stopped")

        finally:
            asyncio.run(self.call_signal("shutdown"))

    async def _run(self):
        """
        Запускает конкурентно две задачи: наблюдение за
        изменениями в файле (если нет флага `--release`) и получение событий
        """
        await self.listen_events()

    async def observe_files_changing(self) -> None:
        """
        Если запуск не содержит флаг `--release`,
        то будет будет следить за изменениями в фалйе.
        Реализация перезагрузки находится в проекте бота
        """
        if "--release" not in sys.argv:
            async for changes in watchgod.awatch(self.observing_path):
                print(changes)

    async def listen_events(self):
        """
        Получает события с помощью одного из генераторов событий.
        После получение вызывает метод по обработке события каждым `EventHandler`'ом
        """
        await self.events_generator.setup()
        async for events in self.events_generator:
            for event in events:
                asyncio.create_task(self.run_through_event_handlers(event))

    async def run_through_event_handlers(
        self, event: vkquick.events_generators.event.Event
    ) -> None:
        """

        """
        # TODO: Handling info scheme
        tasks = [
            asyncio.create_task(event_handler.handle_event(event))
            for event_handler in self.event_handlers
        ]
        handling_info = await asyncio.gather(*tasks)
        self.show_debug_info(event, handling_info)

    def show_debug_info(
        self,
        event: vkquick.events_generators.event.Event,
        handling_info: ty.List[
            vkquick.event_handling.handling_info_scheme.HandlingInfoScheme
        ],
    ):
        if "--release" not in sys.argv:
            if self.debug_filter(event):
                time_header = datetime.datetime.now().strftime(
                    "-- %H:%M:%S %d-%m-%Y"
                )
                debug_info = f"-> {event.type} {sty.fg.li_black + time_header + sty.fg.rs}\n"
                debug_info += (
                    sty.fg.li_black
                    + os.get_terminal_size().columns * "="
                    + sty.fg.rs
                    + "\n\n"
                )
                handling_messages: ty.List[str] = []
                for scheme in handling_info:
                    if scheme["is_correct_event_type"]:
                        handling_message = self._build_event_handler_message(
                            scheme
                        )
                        if scheme["are_filters_passed"]:
                            handling_messages.insert(0, handling_message)
                        else:
                            handling_messages.append(handling_message)

                handling_message = (
                    "\n"
                    + sty.fg.li_black
                    + os.get_terminal_size().columns * "-"
                    + sty.fg.rs
                    + "\n\n"
                ).join(handling_messages)
                vkquick.utils.clear_console()
                print(debug_info + handling_message)

    @staticmethod
    def _build_event_handler_message(
        scheme: vkquick.event_handling.handling_info_scheme.HandlingInfoScheme,
    ) -> str:
        header_color = (
            sty.fg.green if scheme["are_filters_passed"] else sty.fg.red
        )
        header = f"[{header_color + scheme['handler'].reaction.__name__ + sty.fg.rs}]\n"
        filters_decisions: ty.List[str] = [
            f"{sty.fg.yellow + decision[2] + sty.fg.rs}: {decision[1]}"
            for decision in scheme["filters_decision"]
        ]
        filters_decisions: str = "\n".join(filters_decisions)
        arguments: ty.List[str] = [
            f"\n    > {sty.fg.cyan + name + sty.fg.rs}: {value!s}"
            for name, value in scheme["passed_arguments"].items()
        ]
        arguments: str = "".join(arguments)
        return header + filters_decisions + arguments

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

    @staticmethod
    def default_debug_filter(
        event: vkquick.events_generators.event.Event,
    ) -> bool:
        if event.type in ("message_new", "message_edit"):
            return True
