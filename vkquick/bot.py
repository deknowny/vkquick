import asyncio
import logging
import json
from dataclasses import dataclass, field
from typing import Union
from typing import List

import click
from pygments import highlight, lexers, formatters
from pygments.formatters.terminal import TERMINAL_COLORS
from pygments.token import string_to_tokentype

from .api import APIMerging, API
from .lp import LongPoll
from .signal import SignalsList, Signal
from .reaction import ReactionsList, Reaction
from .annotypes import Annotype


TERMINAL_COLORS[string_to_tokentype("String")] =  ('gray', '_')
TERMINAL_COLORS[string_to_tokentype("Token.Literal.Number")] = ('yellow', '_')
TERMINAL_COLORS[string_to_tokentype("Token.Keyword.Constant")] = ('red', '_')
TERMINAL_COLORS[string_to_tokentype("Token.Name.Tag")] =  ('cyan', '_')


@dataclass
class Bot(APIMerging, Annotype):
    """
    Main LongPoll, API, commands and signals handler
    """

    token: str
    group_id: int

    debug: bool

    version: Union[float, int] = 5.124
    wait: int = 25
    delay: float = 1/20

    signals: List[Signal] = field(default_factory=SignalsList)
    reactions: List[Reaction] = field(default_factory=ReactionsList)


    def __post_init__(self):
        if float(self.version) < 5.103:
            raise ValueError("You can't use API version lower than 5.103")
        self.version = str(self.version)
        self.merge(
            API(
                token=self.token,
                version=self.version,
                delay=self.delay
            )
        )
        self.lp = LongPoll(group_id=self.group_id, wait=self.wait)

        self.lp.merge(self.api)
        self.reaload_now = False

    @staticmethod
    def prepare(argname, event, func, bot, bin_stack):
        return bot

    def debug_out(self, string, **kwargs):
        """
        Prins only if debug=True
        """
        if self.debug:
            print(string, **kwargs)

    def run(self):
        """
        Runs LP process
        """
        asyncio.run(self.signals.resolve("startup"))
        asyncio.run(self._process_handler())
        asyncio.run(self.signals.resolve("shutdown"))

    async def _files_changing_check(self):
        """
        Raise RuntimeError after files changing to stop bot
        """
        while not self.reaload_now:
            await asyncio.sleep(0)
        raise RuntimeError()

    async def _process_handler(self):
        try:
            await asyncio.gather(self._files_changing_check(), self._run())
        except RuntimeError:
            return

    async def _run(self):
        """
        Run in `run` by self.run()
        """
        async for events in self.lp:
            for event in events:

                if self.debug and self.reactions.has_event(event.type):
                    click.clear()
                    data = json.dumps(event._mapping, ensure_ascii=False, indent=4)
                    data = highlight(
                        data,
                        lexers.JsonLexer(),
                        formatters.TerminalFormatter(bg="light")
                    )
                    print("=" * 18, "Below is the event\n", sep="\n", end="=" * 18 + "\n")
                    print(data)
                    print("=" * 18, "Above is the event\n", sep="\n", end="=" * 18 + "\n")
                    click.clear()


                show = await self.reactions.resolve(event, self)
