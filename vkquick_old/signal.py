"""
Обработчики сигналов (собственных событий)
"""
from asyncio import iscoroutinefunction as icf
from dataclasses import dataclass

from vkquick import current


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
            return await self.code(*args, **kwargs)
        else:
            return self.code(*args, **kwargs)


class SignalsList(list):
    """
    Список обрабатываемых сигналов
    """

    async def resolve(self, name: str, /, *args, **kwargs):
        """
        Call a signal with name `name` and params *args and **kwargs
        """
        for signal in self:
            if signal.name == name:
                return await signal.run(*args, **kwargs)


async def signal(name, *args, **kwargs):
    """
    Вызов сигнала с именем name и параметрами `*args` и `**kwargs`
    """
    return await current.bot.signals.resolve(name, *args, **kwargs)
