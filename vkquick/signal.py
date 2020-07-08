"""
Обработчики сигналов (собственных событий)
"""
from asyncio import iscoroutinefunction as icf
from asyncio import create_task
from dataclasses import dataclass
from typing import Any


@dataclass
class Signal:
    """
    Образец обработчика сигнала
    """

    name: str

    def __call__(self, code):
        self.code = code

        return self

    async def run(self, *args, **kwargs):
        if icf(self.code):
            create_task(self.code(*args, **kwargs))
        else:
            self.code(*args, **kwargs)


class SignalsList(list):
    """
    Список обрабатываемых сигналов
    """

    async def resolve(self, name: str, /,  *args, **kwargs):
        """
        Call a signal with name `name` and params *args and **kwargs
        """
        for signal in self:
            if signal.name == name:
                await signal.run(*args, **kwargs)
