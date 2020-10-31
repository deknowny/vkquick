import abc
import dataclasses
import enum
import typing as ty

import vkquick.events_generators.event
import vkquick.event_handling.event_handler
import vkquick.utils


@dataclasses.dataclass
class Decision:
    passed: bool
    description: str


class DecisionStatus(enum.Enum):
    ...


@dataclasses.dataclass
class FilterResponse:
    status_code: DecisionStatus
    decision: Decision
    extra: vkquick.utils.AttrDict = dataclasses.field(
        default_factory=vkquick.utils.AttrDict
    )


class Filter(abc.ABC):
    @abc.abstractmethod
    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> FilterResponse:
        """
        Определяет, подходит ли событие по критериями фильтра
        """

    def __call__(self, event_handler):
        if not isinstance(
            event_handler, vkquick.event_handling.event_handler.EventHandler
        ):
            raise TypeError(
                "Filters can be used only for `EventHandler` and its subclasses"
            )
        event_handler.filters.append(self)
        return event_handler
