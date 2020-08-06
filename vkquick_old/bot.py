"""
Основная точка запуска любого бота
"""
import asyncio
import json
from dataclasses import dataclass, field
from typing import Union
from typing import List

import click
from pygments import highlight, lexers, formatters
from pygments.formatters.terminal import TERMINAL_COLORS
from pygments.token import string_to_tokentype

from .api import API
from .lp import LongPoll
from .signal import SignalsList, Signal
from .reaction import ReactionsList, Reaction
from .annotypes import Annotype
from . import current


TERMINAL_COLORS[string_to_tokentype("String")] = ("gray", "_")
TERMINAL_COLORS[string_to_tokentype("Token.Literal.Number")] = ("yellow", "_")
TERMINAL_COLORS[string_to_tokentype("Token.Keyword.Constant")] = ("red", "_")
TERMINAL_COLORS[string_to_tokentype("Token.Name.Tag")] = ("cyan", "_")


@dataclass
class Bot(Annotype):
    """
    Основной менеджер событий LongPoll,
    сигналов, API запросов и в целом работы бота
    """

    token: str
    """
    Токен пользователя/группы
    """

    group_id: int
    """
    Айдификатор группы, с которым будут
    связаны LongPoll события
    """

    debug: bool
    """
    Режим дебага в терминале
    """

    config: dict = field(default_factory=dict)
    """
    Общие настройки бота (дополнительно)
    """

    version: Union[float, str] = 5.124
    """
    Версия API
    """

    wait: int = 25
    """
    Время ожидания ответа LongPoll события
    """

    owner: str = "group"
    """
    Тип владельца токена. group/user
    """

    URL: str = "https://api.vk.com/method/"
    """
    URL API запросов
    """

    signals: List[Signal] = field(default_factory=SignalsList)
    """
    Список обрабатываемых сигналов
    """

    reactions: List[Reaction] = field(default_factory=ReactionsList)
    """
    Список обрабатываемых реакций
    """

    def __post_init__(self):
        current.bot = self
        if float(self.version) < 5.103:
            raise ValueError("You can't use API version lower than 5.103")
        self.version = str(self.version)
        current.api = API(
            token=self.token,
            version=self.version,
            owner=self.owner,
            group_id=self.group_id,
            URL=self.URL,
        )
        self.lp = LongPoll(group_id=self.group_id, wait=self.wait)

        self.reload_now = False

    @staticmethod
    def prepare(argname, event, func, bin_stack):
        return current.bot

    def debug_out(self, string, **kwargs):
        """
        Проивзодит вывод, если включен режим дебага
        """
        if self.debug:
            print(string, **kwargs)

    def run(self):
        """
        Запускает LongPoll процесс,
        вызывая перед этим `startup`,
        а в конце и `shutdown` сигналы
        """
        asyncio.run(self.signals.resolve("startup"))

        while True:
            try:
                asyncio.run(self._process_handler())
            except (RuntimeError, KeyboardInterrupt):
                break
            finally:
                asyncio.run(self.signals.resolve("shutdown"))

    async def _files_changing_check(self):
        """
        Поднимает RuntimeError после изменений
        в директории бота для того, чтобы остановиться
        """
        while not self.reload_now:
            await asyncio.sleep(0)
        raise RuntimeError()

    async def _process_handler(self):
        """
        Запускает две таски:

        1. Процесс прослушивания LongPoll и обработки событий реакциями
        1. Слежку за изменением файлов по "переменной состояния"
        """
        await asyncio.gather(self._files_changing_check(), self._run())

    async def _run(self):
        """
        Процесс прослушивания LongPoll и обработки событий реакциями
        """
        async for events in self.lp:
            for event in events:

                if self.debug and self.reactions.has_event(event.type):
                    click.clear()

                    data = json.dumps(
                        event._mapping, ensure_ascii=False, indent=4
                    )
                    data = highlight(
                        data,
                        lexers.JsonLexer(),
                        formatters.TerminalFormatter(bg="light"),
                    )
                    self.debug_out(
                        f"{'=' * 35}\nBelow is the current handled event\n{'=' * 35}\n"
                    )
                    # print("=" * 35, "Below is the current handled event\n", sep="\n", end="=" * 35 + "\n")
                    self.debug_out(data.strip())
                    self.debug_out(
                        f"{'=' * 35}\nAbove is the current handled event\n{'=' * 35}\n"
                    )

                asyncio.create_task(self.reactions.resolve(event))
