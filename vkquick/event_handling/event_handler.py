from __future__ import annotations
import inspect
import time
import traceback
import typing as ty

import vkquick.events_generators.event
import vkquick.base.payload_argument
import vkquick.base.filter
import vkquick.utils
import vkquick.event_handling.handling_info_scheme


class EventHandler:
    """
    Обертка для создания реакций на события.
    Фактическая инициализация разбивается на 2 этапа:

    1. Создание инстанса. `event_types` состоит из возможных обрабатываемых событий.
    Если ничего не передано -- обрабатываются все события
    2. Декорирование (в `__call__` передать функцию).

    После чего можно передать объект в инициализатор `Bot`
    """

    def __init__(self, *event_types) -> None:
        self.event_types = event_types or ...
        self.filters: ty.List[vkquick.base.filter.Filter] = []
        self.payload_arguments = {}
        self.reaction_arguments = {}

    def __call__(
        self, reaction: ty.Callable[..., ty.Union[ty.Awaitable, None]]
    ) -> EventHandler:
        self.reaction = reaction
        self._capture_reaction_arguments()
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
        start_stamp = time.time()
        is_correct_event_type = self.is_correct_event_type(event)
        if not is_correct_event_type:
            end_stamp = time.time()
            return vkquick.event_handling.handling_info_scheme.HandlingInfoScheme(
                handler=self,
                is_correct_event_type=False,
                all_filters_passed=False,
                taken_time=end_stamp - start_stamp,
            )

        passed_all, filters_response = await self.run_trough_filters(event)
        if not passed_all:
            end_stamp = time.time()
            return vkquick.event_handling.handling_info_scheme.HandlingInfoScheme(
                handler=self,
                is_correct_event_type=True,
                all_filters_passed=False,
                filters_response=filters_response,
                taken_time=end_stamp - start_stamp,
            )

        reaction_arguments = await self.init_reaction_arguments(event)
        try:
            await self.call_reaction(event, reaction_arguments)
        except Exception:
            exception = traceback.format_exc()
        else:
            exception = ""
        finally:
            end_stamp = time.time()
            return vkquick.event_handling.handling_info_scheme.HandlingInfoScheme(
                handler=self,
                is_correct_event_type=True,
                all_filters_passed=True,
                filters_response=filters_response,
                passed_arguments=reaction_arguments,
                taken_time=end_stamp - start_stamp,
                exception_text=exception,  # NOTE: Что делать с `BaseException` кейсом?
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
    ) -> ty.Tuple[
        bool, ty.List[ty.Tuple[str, vkquick.base.filter.FilterResponse]]
    ]:
        """
        Пропускает событие через все фильтры. Возвращает кортеж из значений:

        * Прошли ли абсолютно все события под фильтр
        * Список, описанный под полем `HandlingInfoScheme.filters_decision`
        """
        passed_all = True
        filters_decision = []
        for filter_ in self.filters:
            filter_response = await vkquick.utils.sync_async_run(
                filter_.make_decision(event)
            )
            decision = (filter_.__class__.__name__, filter_response)
            filters_decision.append(decision)
            if not filter_response.decision.passed:
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
                value, vkquick.base.payload_argument.PayloadArgument,
            ):
                reaction_arguments[name] = await vkquick.utils.sync_async_run(
                    value.init_value(event)
                )
        return reaction_arguments

    def _capture_reaction_arguments(self) -> None:
        """
        Если тайпинг аргумента не инстанс,
        а должен быть (поле `always_be_instance`),
        инстанс создастся автоматически
        """
        reaction_parameters = inspect.signature(self.reaction).parameters
        for name, value in reaction_parameters.items():
            if value.default != value.empty:
                typing_type = value.default
            else:
                typing_type = value.annotation
            if inspect.isclass(typing_type):
                self.reaction_arguments[name] = typing_type()
            else:
                self.reaction_arguments[name] = typing_type

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
