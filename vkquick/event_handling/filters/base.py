import abc
import typing as ty

import vkquick.events_generators.event


class Filter(abc.ABC):
    @abc.abstractmethod
    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Tuple[bool, str]:
        """
        Определяет, подходит ли событие по критериями фильтра
        """
