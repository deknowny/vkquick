from __future__ import annotations
import asyncio
import inspect
import typing as ty

from vkquick import utils

from . import handling_info, event as event_, payload_argument
from vkquick.event_handling import message


class EventHandler:
    """
    Обертка для всех обработчиков событий

    init:
        *events_type:
            Имена обрабатываемых событий (`event.type`)

    fields:
        event_types
            Имена обрабатываемых событий (`event.type`)
    # TODO
    """

    def __init__(self, *event_types) -> None:
        self.event_types = event_types
        self._filters = []

    def __call__(self, func: ty.Callable[..., ty.Any]) -> EventHandler:
        """
        Вызывать сразу после инициализации
        """
        self.func = func

        # Раскрытие алиасов (MyType == MyType())
        self._reveal_aliases(func)

        return self

    def _reveal_aliases(
        self, func: ty.Callable[..., ty.Union[str, message.Message]],
    ):
        self._func_parameters = dict(inspect.signature(func).parameters)
        for name, value in self._func_parameters.items():
            if inspect.isclass(value.annotation):
                self._func_parameters[name] = value.annotation()
            else:
                self._func_parameters[name] = value.annotation

    async def handle_event(
        self, event: event_.Event
    ) -> handling_info.HandlingInfo:
        """
        Вызывается для обработки событий
        """
        # Тип события соответствует допутимым событям
        if event.type in self.event_types or not self.event_types:
            # Основная информация о процессе валидации.
            # В оптимизированной обработке отсутствует
            handled_info = handling_info.HandlingInfo(
                filters_state={},
                arguments={},
                handler_decision=(
                    True,
                    f"Событие находится среди обрабатываемых событий {list(self.event_types)}",
                ),
            )
            async for decision in self._run_through_filters(event):
                # decision[0] -- имя фильтра
                # decision[1] -- решение фильтра
                handled_info["filters_state"][decision[0]] = decision[1]
                if not decision[1][0]:  # Фильтр не пройден
                    return handled_info

            # Аргументы, передаваемые в указанный обработчик из `__call__`
            arguments = {
                key: value
                async for key, value in self._init_func_arguments(
                    event, self._func_parameters
                )
            }
            handled_info["arguments"] = arguments
            asyncio.create_task(utils.sync_async_run(self.func(**arguments)))
            return handled_info
        else:
            return handling_info.HandlingInfo(
                filters_state={},
                arguments={},
                handler_decision=(
                    False,
                    f"Не подходит тип события, ожидалось одно из {list(self.event_types)}",
                ),
            )

    async def handle_event_optimized(self, event: event_.Event) -> None:
        """
        Оптимизированная версия `handle_event`.
        Не собирает информацию о процессах фильтрации
        и переданных аргументах и не выводит ее
        """
        if event.type in self.event_types or not self.event_types:
            async for decision in self._run_through_filters(event):
                if not decision[1][0]:  # Фильтр не пройден
                    return
            # Аргументы, передаваемые в указанный обработчик из `__call__`
            arguments = {
                key: value
                async for key, value in self._init_func_arguments(
                    event, self._func_parameters
                )
            }
            asyncio.create_task(utils.sync_async_run(self.func(**arguments)))

    async def _run_through_filters(
        self, event: event_.Event
    ) -> ty.AsyncGenerator[str, ty.Tuple[bool, str], None, None]:
        """
        Прогоняет событие по заданным в обработчик фильтрам.
        Yield'ит решение фильтра и его имя
        """
        for filter_ in self._filters:
            filter_decision = await filter_.decide(event)
            yield filter_.__name__, filter_decision

    async def _init_func_arguments(
        self,
        event: event_.Event,
        func_parameters: ty.Dict[str, payload_argument.PayloadArgument],
    ) -> ty.AsyncGenerator[ty.Tuple[str, ty.Any], None, None]:
        """
        Собирает аргументы для функции, основываясь на тайпингах.
        Yield'ит имя аргумента и его значение
        """
        for name, value in func_parameters.items():
            argument_value = await utils.sync_async_run(
                value.make_value(event)
            )
            yield name, argument_value
