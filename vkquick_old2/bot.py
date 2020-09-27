"""
Основная точка запуска любого бота
"""
import asyncio
import dataclasses
import os
import typing as ty

import vkquick.events_handling
from . import signals, current
from vkquick import exceptions

DEBUG_LOCAL_SEPARATOR = "=" * os.get_terminal_size().columns
DEBUG_GLOBAL_SEPARATOR = "\n".join([DEBUG_LOCAL_SEPARATOR] * 2)


@dataclasses.dataclass
class Bot:
    """
    """

    signals_handlers: ty.List[signals.SignalHandler] = dataclasses.field(
        default_factory=list
    )
    """
    Список обрабатчиков сигналов
    """

    events_handlers: ty.List[vkquick.events_handling.EventHandler] = dataclasses.field(
        default_factory=list
    )
    """
    Список обрабатчиков событий
    """

    system_help: str = "vq::help"
    """
    Префикс на 
    """

    def run(self) -> ty.NoReturn:
        asyncio.run(self.handle_signal(signals.BuiltinSignals.STARTUP))
        try:
            while True:
                try:
                    asyncio.run(self._run())
                except exceptions.BotReloadError:
                    break
        finally:
            asyncio.run(self.handle_signal(signals.BuiltinSignals.SHUTDOWN))

    async def _run(self) -> None:
        await asyncio.gather(
            self.longpoll_listening(), self.observe_reloading_state()
        )

    async def longpoll_listening(self):
        async with current.lp as lp:
            async for events in lp:
                for event in events:
                    asyncio.create_task(self.handle_event(event))

    async def handle_signal(
        self,
        signal_name: ty.Union[str, signals.BuiltinSignals],
        *args,
        **kwargs
    ) -> ty.Any:
        ...

    async def handle_event(self, event: vkquick.events_handling.Event) -> None:
        print(event)
        for reaction_handler in self.events_handlers:
            asyncio.create_task(reaction_handler.handle_event(event))

    async def observe_reloading_state(self) -> None:
        while not current.reload_now:
            await asyncio.sleep(0)
        raise exceptions.BotReloadError()

    def get_event_handler_by_name(self, name: str) -> ty.Optional[vkquick.events_handling.event_handler.EventHandler]:
        for handler in self.events_handlers:
            if handler.func.__name__.lower() == name.lower():
                return handler
        return None


class BotRelease(Bot):
    async def handle_event(self, event: dict) -> None:
        ...

    async def observe_reloading_state(self) -> None:
        pass

    async def _run(self):
        await self.longpoll_listening()

    #
    #
    # ######
    #
    # def debug_out(self, string, **kwargs):
    #     """
    #     Проивзодит вывод, если включен режим дебага
    #     """
    #     if self.debug:
    #         print(string, **kwargs)
    #
    # def run(self):
    #     """
    #     Запускает LongPoll процесс,
    #     вызывая перед этим `startup`,
    #     а в конце и `shutdown` сигналы
    #     """
    #     asyncio.run(self.signals.resolve("startup"))
    #
    #     while True:
    #         try:
    #             asyncio.run(self._process_handler())
    #         except (RuntimeError, KeyboardInterrupt):
    #             break
    #         finally:
    #             asyncio.run(self.signals.resolve("shutdown"))
    #
    # async def _files_changing_check(self):
    #     """
    #     Поднимает RuntimeError после изменений
    #     в директории бота для того, чтобы остановиться
    #     """
    #     while not self.reload_now:
    #         await asyncio.sleep(0)
    #     raise RuntimeError()
    #
    # async def _process_handler(self):
    #     """
    #     Запускает две таски:
    #
    #     1. Процесс прослушивания LongPoll и обработки событий реакциями
    #     1. Слежку за изменением файлов по "переменной состояния"
    #     """
    #     await asyncio.gather(self._files_changing_check(), self._run())
    #
    # async def _run(self):
    #     """
    #     Процесс прослушивания LongPoll и обработки событий реакциями
    #     """
    #     async for events in self.lp:
    #         for event in events:
    #
    #             if self.debug and self.reactions.has_event(event.type):
    #                 click.clear()
    #
    #                 data = json.dumps(
    #                     event._mapping, ensure_ascii=False, indent=4
    #                 )
    #                 data = highlight(
    #                     data,
    #                     lexers.JsonLexer(),
    #                     formatters.TerminalFormatter(bg="light"),
    #                 )
    #                 self.debug_out(
    #                     f"{'=' * 35}\nBelow is the current handled event\n{'=' * 35}\n"
    #                 )
    #                 # print("=" * 35, "Below is the current handled event\n", sep="\n", end="=" * 35 + "\n")
    #                 self.debug_out(data.strip())
    #                 self.debug_out(
    #                     f"{'=' * 35}\nAbove is the current handled event\n{'=' * 35}\n"
    #                 )
    #
    #             asyncio.create_task(self.reactions.resolve(event))
