import abc
import dataclasses
import enum
import typing as ty

import vkquick.events_generators.event
import vkquick.event_handling.event_handler
import vkquick.utils


@dataclasses.dataclass(frozen=True)
class Decision:
    passed: bool
    description: str


class DecisionStatus(enum.Enum):
    ...


@dataclasses.dataclass(frozen=True)
class FilterResponse:
    """
    Ответ, который дает фильтр после обработки события
    """
    status_code: DecisionStatus
    decision: Decision
    extra: vkquick.utils.AttrDict = dataclasses.field(
        default_factory=vkquick.utils.AttrDict
    )


class Filter(abc.ABC):
    """
    Фильтр говорит сам за себя -- он фильтрует
    событие по каким-либо параметрам внутри.
    Помещать фильтр нужно над декоратором обработки реакции.
    После обработки события (методом `make_decision`)
    возвращает специальный объект `FilterResponse`.

    В `Command` статус обработки фильтра может быть использован,
    чтобы задать отдельную реакцию. (Например, нужно, чтобы
    пользователь отправил фотографию. Вы можете быстро
    определить поведение, когда фотография не отправлена)
    """

    @abc.abstractmethod
    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> FilterResponse:
        """
        Определяет, подходит ли событие по критериям фильтра
        """

    def __call__(
        self, event_handler: vkquick.event_handling.event_handler.EventHandler
    ) -> vkquick.event_handling.event_handler.EventHandler:
        """
        Вызывается в момент декорирования.
        Фильтры должны быть указаны над хендлером событий
        """
        if not isinstance(
            event_handler, vkquick.event_handling.event_handler.EventHandler
        ):
            raise TypeError(
                "Filters can be used only for `EventHandler` "
                "and its subclasses. Also all filters should "
                "be above the `EventHandler`/`Command` decorator"
            )
        event_handler.filters.append(self)
        return event_handler
