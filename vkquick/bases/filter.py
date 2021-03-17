from __future__ import annotations

import abc
import typing as ty

if ty.TYPE_CHECKING:
    from vkquick.event_handler.context import EventHandlingContext
    from vkquick.event_handler.handler import EventHandler


class Filter(abc.ABC):

    __accepted_event_types__: ty.FrozenSet[ty.Union[str, int]] = frozenset()

    @abc.abstractmethod
    def make_decision(self, context: EventHandlingContext):
        """
        Определяет, подходит ли событие по критериям фильтра
        """

    def __call__(self, event_handler: EventHandler):
        event_handler.add_filter(self)
