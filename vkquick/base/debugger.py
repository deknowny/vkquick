import abc
import dataclasses
import typing as ty

from vkquick import API
from vkquick.wrappers.message import Message
from vkquick.base.handling_status import HandlingStatus
from vkquick.current import fetch


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
    api: API

    message: Message
    """
    Событие, которое было обработано
    """
    schemes: ty.List[HandlingStatus]
    """
    Набор отчетов об обработке, сформированных обработчиками/командами
    """

    @abc.abstractmethod
    def render(self):
        """
        Основной метод визуализации, выстраивающий
        сообщение для отображения в терминале
        """
