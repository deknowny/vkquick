from __future__ import annotations

import abc
import typing as ty

if ty.TYPE_CHECKING:
    from vkquick.event_handler.context import EventHandlingContext
    from vkquick.event_handler.handler import EventHandler


class Filter(abc.ABC):
    """

    :cvar __accepted_event_types__: Возможные типы событий, которые способен обработать фильтр.
        `Ellipsis` если способен обработать все.
    """

    __accepted_event_types__: ty.Union[
        ty.FrozenSet[ty.Union[str, int]], ty.Type[...]
    ] = frozenset()

    @abc.abstractmethod
    def make_decision(self, ehctx: EventHandlingContext) -> None:
        """
        Определяет, подходит ли событие по критериям фильтра
        """

    def __call__(self, event_handler: EventHandler) -> EventHandler:
        event_handler.add_filter(self)
        return event_handler
