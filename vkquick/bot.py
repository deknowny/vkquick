import asyncio
import sys
import typing as ty

import vkquick.current
import vkquick.event_handling.event_handler
import vkquick.signal_handling.signal_handler
import vkquick.events_generators.event
import vkquick.exceptions
import vkquick.utils


class Bot:

    events_generator = vkquick.current.fetch("events_generator", "cb", "lp")

    def __init__(
        self,
        *,
        signal_handlers: ty.List[
            vkquick.signal_handling.signal_handler.SignalHandler
        ],
        event_handlers: ty.List[
            vkquick.event_handling.event_handler.EventHandler
        ],
    ):
        self.signal_handlers = signal_handlers
        self.event_handlers = event_handlers
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
        finally:
            asyncio.run(self.call_signal("shutdown"))

    async def _run(self):
        """
        Запускает конкурентно две задачи: наблюдение за
        изменениями в файле (если нет флага `--release`) и получение событий
        """
        await asyncio.gather(
            self.observe_files_changing(), self.listen_events()
        )

    async def observe_files_changing(self) -> None:
        """
        Если запуск не содержит флаг `--release`,
        то будет будет следить за изменениями в фалйе.
        Реализация перезагрузки находится в проекте бота
        """
        if "--release" not in sys.argv:
            while not self.reload_now:
                await asyncio.sleep(0)
            raise vkquick.exceptions.BotReloadNow()

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
        handling_info = await asyncio.wait(tasks)

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
