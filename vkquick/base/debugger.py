import abc
import dataclasses
import typing as ty

import vkquick.event_handling.handling_info_scheme
import vkquick.events_generators


@dataclasses.dataclass
class Debugger(abc.ABC):
    """
    Дебаггер -- терминальный визуализатор команд,
    наглядно показывающий, что произошло во время
    обработки события: подходит ли его тип, каково
    решение фильтров самого обработчика, какие
    аргументы были переданы в реакцию и была ли реакция вызвана
    вообще
    """

    event: vkquick.events_generators.event.Event
    """
    Событие, которое было обработано
    """
    schemes: ty.List[
        vkquick.event_handling.handling_info_scheme.HandlingInfoScheme
    ]
    """
    Набор отчетов об обработке, сформированных обработчиками/командами
    """

    @abc.abstractmethod
    def render(self):
        """
        Основной метод визуализации, выстраивающий
        сообщение для отображения в терминале
        """
