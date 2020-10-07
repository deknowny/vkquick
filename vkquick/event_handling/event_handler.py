from __future__ import annotations
import asyncio
import inspect
import typing as ty

import vkquick.events_generators.event
import vkquick.event_handling.reaction_argument.payload_arguments.base
import vkquick.event_handling.filters.base
import vkquick.utils
import vkquick.event_handling.handling_info_scheme


class EventHandler:
    """
    Обертка для создания реакций но события.
    Фактическая инициализация разбивается на 2 этапа:

    1. Создание инстанса. `event_types` состоит
    из возможных обрабатываемых событий.
    Если ничего не передано -- обрабатываются все события
    2. Декорирование (в `__call__` передать функцию).

    После чего можно передать объект в инициализатор `Bot`
    """

    def __init__(self, *event_types) -> None:
        self.event_types = event_types or ...
        self.filters: ty.List[vkquick.event_handling.filters.base.Filter] = []

    def __call__(
        self, reaction: ty.Callable[..., ty.Union[ty.Awaitable, None]]
    ) -> EventHandler:
        self.reaction = reaction
        self.reaction_arguments = self._convert_reaction_arguments(reaction)
        return self

    async def handle_event(
        self, event: vkquick.events_generators.event.Event
    ) -> vkquick.event_handling.handling_info_scheme.HandlingInfoScheme:
        """
        Процесс обработки события.

        1. Проверка на корректность `event.type`
        2. Прошло ли событие все фильтры
        3. Инициализация аргументов для реакции
        """
        is_correct_event_type = self.is_correct_event_type(event)
        if not is_correct_event_type:
            return vkquick.event_handling.handling_info_scheme.HandlingInfoScheme(
                is_correct_event_type=False,
                is_filters_passed=False,
                filters_decision=[],
                passed_arguments={},
            )

        passed_all, filters_decision = await self.run_trough_filters(event)
        if not passed_all:
            return vkquick.event_handling.handling_info_scheme.HandlingInfoScheme(
                is_correct_event_type=True,
                is_filters_passed=False,
                filters_decision=filters_decision,
                passed_arguments={},
            )

        reaction_arguments = await self.init_reaction_arguments(event)
        asyncio.create_task(self.call_reaction(event, reaction_arguments))
        return vkquick.event_handling.handling_info_scheme.HandlingInfoScheme(
            is_correct_event_type=True,
            is_filters_passed=False,
            filters_decision=filters_decision,
            passed_arguments=reaction_arguments,
        )

    def is_correct_event_type(
        self, event: vkquick.events_generators.event.Event
    ) -> bool:
        """
        Проверяет, предназначена ли реакция
        для обработки событий с типом из `event.type`
        """
        return self.event_types is Ellipsis or event.type in self.event_types

    async def run_trough_filters(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Tuple[bool, ty.List[ty.Tuple[bool, str, str]]]:
        """
        Пропускает событие через все фильтры. Возвращает кортеж из значений:

        * Прошли ли абсолютно все события под фильтр
        * Список, описанный под полем `HandlingInfoScheme.filters_decision`
        """
        passed_all = True
        filters_decision = []
        for filter_ in self.filters:
            passed, description = await vkquick.utils.sync_async_run(
                filter_.make_decision(event)
            )
            decision = (passed, description, filter_.__name__)
            filters_decision.append(decision)
            if not passed:
                passed_all = False
                break

        return passed_all, filters_decision

    async def init_reaction_arguments(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Dict[str, ty.Any]:
        """
        Инициализирует значения для аргументов функции.
        В этой реализации только для `PayloadArgument`
        """
        reaction_arguments = {}
        for name, value in self.reaction_arguments.items():
            if isinstance(
                value,
                vkquick.event_handling.reaction_argument.payload_arguments.base.PayloadArgument,
            ):
                reaction_arguments[name] = await vkquick.utils.sync_async_run(
                    value.init_value(event)
                )
        return reaction_arguments

    @staticmethod
    def _convert_reaction_arguments(reaction) -> ty.Dict[str, ty.Any]:
        """
        Если тайпинг аргумента не инстанс,
        а должен быть (поле `always_be_instance`),
        инстанс создастся автоматически
        """
        reaction_parameters = inspect.signature(reaction).parameters
        reaction_arguments = {}
        for name, value in reaction_parameters.items():
            if inspect.isclass(value.annotation):
                reaction_arguments[name] = value.annotation()
            else:
                reaction_arguments[name] = value.annotation

        return reaction_arguments

    async def call_reaction(
        self,
        _: vkquick.events_generators.event.Event,
        arguments: ty.Dict[str, ty.Any],
    ) -> None:
        """
        Вызывает реакцию с аргументами из `arguments`. Вынесено в отдельный метод
        для удобного переопределения в `Command`.
        Там есть дополнительная логика с тем, что вернула реакция
        """
        await vkquick.utils.sync_async_run(self.reaction(**arguments))
