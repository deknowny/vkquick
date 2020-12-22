import abc
import dataclasses
import typing as ty

from vkquick import API
from vkquick.events_generators.event import Event
from vkquick.base.handling_status import HandlingStatus


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
        self, api: API, event: Event, schemes: ty.List[HandlingStatus]
    ) -> None:
        self._api = api
        self._message = event.msg
        self._schemes = schemes

    @abc.abstractmethod
    def render(self):
        """
        Основной метод визуализации, выстраивающий
        сообщение для отображения в терминале
        """
