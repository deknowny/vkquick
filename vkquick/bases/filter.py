from __future__ import annotations

import abc
import typing as ty

if ty.TYPE_CHECKING:
    from vkquick.handlers import EventHandlingContext


class Filter(abc.ABC):
    @abc.abstractmethod
    def make_decision(self, context: EventHandlingContext):
        """
        Определяет, подходит ли событие по критериям фильтра
        """
