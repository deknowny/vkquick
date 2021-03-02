import abc
import dataclasses
import typing as ty

from vkquick.base.handling_status import HandlingStatus
from vkquick.events_generators.event import Event
from vkquick.wrappers.message import Message


@dataclasses.dataclass
class Debugger(abc.ABC):
    """
    Дебаггер -- терминальный визуализатор команд,
    наглядно показывающий, что произошло во время
    обработки события: подходит ли его тип, каково
    решение фильтров самого обработчика, какие
    аргументы были переданы в реакцию, и была ли реакция вызвана
    вообще
    """

    def __init__(
        self,
        sender_name: str,
        message_text: str,
        schemes: ty.List[HandlingStatus],
    ) -> None:
        self._sender_name = sender_name
        self._message_text = message_text
        self._schemes = schemes

    @abc.abstractmethod
    async def startup(self):
        ...

    @abc.abstractmethod
    async def shutdown(self):
        ...

    @abc.abstractmethod
    async def render(self):
        """
        Основной метод визуализации, выстраивающий
        сообщение для отображения в терминале
        """
