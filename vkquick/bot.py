import asyncio
from dataclasses import dataclass, field
from typing import Union
from typing import List

from .api import APIMerging, API
from .lp import LongPoll
from .signal import SignalsList, Signal
from .reaction import ReactionsList, Reaction


@dataclass
class Bot(APIMerging):
    """
    Main LongPoll, API, commands and signals handler
    """
    token: str
    group_id: int
    version: Union[float, int] = 5.124
    wait: int = 25

    signals: List[Signal] = field(default_factory=SignalsList)
    reactions: List[Reaction] = field(default_factory=ReactionsList)


    def __post_init__(self):
        if self.version < 5.103:
            raise ValueError(
                "You can't use API version lower than 5.103"
            )
        self.version = str(self.version)
        self.merge(
            API(token=self.token, version=self.version)
        )
        self.lp = LongPoll(
            group_id=self.group_id, wait=self.wait
        )

        self.lp.merge(self.api)
        self.reaload_now = False

    async def _files_changing_check(self):
        while not self.reaload_now:
            await asyncio.sleep(0)
        raise RuntimeError()


    def run(self):
        """
        Runs LP process
        """
        asyncio.run(self.signals.resolve("startup"))
        asyncio.run(self._process_handler())
        asyncio.run(self.signals.resolve("shutdown"))

    async def _process_handler(self):
        try:
            await asyncio.gather(
                self._files_changing_check(),
                self._run()
            )
        except RuntimeError:
            return

    async def _run(self):
        """
        Run in `run` by self.run()
        """
        async for events in self.lp:
            for event in events:
                await self.reactions.resolve(event, self)
