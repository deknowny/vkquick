from __future__ import annotations

import abc
import typing as ty

if ty.TYPE_CHECKING:
    from vkquick.event_handler.context import EventHandlingContext
    from vkquick.event_handler.handler import EventHandler


class Filter(abc.ABC):
    """
    Фильтр — удобная валидация обработчика событий.
    Например, для сообщения можно поставить фильтр,
    который будет игнорировать сообщения от групп,
    или же фильтр, который проверяет сообщение на текст
    (обычная команда).
    """

    accepted_event_types: ty.FrozenSet[ty.Union[str, int]] = frozenset()
    """
    Возможные типы событий, которые способен обработать фильтр.
    Пустое множество событий означает, что фильтр способен обработать любое
    событие
    """

    @abc.abstractmethod
    async def make_decision(self, ehctx: EventHandlingContext) -> None:
        """
        Определяет, подходит ли событие по критериям фильтра.
        Если событие не подходи

        Arguments:
            ehctx: Контекст обработки хэндлером
        """

    def __call__(self, event_handler: EventHandler) -> EventHandler:
        """
        Вызывается в момент декорирования. По умолчанию просто добавляет
        себя в фильтры, возвращая принятый инстнанс хэндлера для продолжения
        декорирования другими фильтрами

        Arguments:
            event_handler: Обработчик события, куда прикрепляется фильтр

        Returns:
            Тот же обработчик с события, куда был добавлен сам фильтр
        """
        event_handler.add_filter(self)
        return event_handler
