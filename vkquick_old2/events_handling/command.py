from __future__ import annotations
import asyncio
import dataclasses
import inspect
import pathlib
import re
import typing as ty

from . import (
    handling_info,
    event as event_,
    text_argument,
    payload_argument,
)
from vkquick.event_handling import message

from vkquick import utils, current
from vkquick.events_handling.event_handler import EventHandler


@dataclasses.dataclass
class Command(EventHandler):
    """
    Easy command creation  # TODO
    """

    # TODO: auto re.escape
    case_sensitive: bool = False
    ignore_editing: bool = False
    allow_editing: bool = True
    title: ty.Optional[str] = None
    names: ty.Iterable[str] = ()
    prefixes: ty.Iterable[str] = ()
    help_prefixes: ty.Iterable[str] = ("vq::",)
    help_names: ty.Iterable[str] = ("help", "помощь")
    help_command_names: ty.Iterable[str] = ()
    description: ty.Optional[str] = None
    on_help: ty.Optional[
        ty.Callable[[event_.Event], ty.Union[str, message.Message]]
    ] = None
    on_invalid_parameter: ty.Dict[
        str, ty.Callable[[event_.Event], ty.Union[str, message.Message]]
    ] = dataclasses.field(default_factory=dict)
    usage_examples: ty.Optional[ty.List[ty.Tuple[str, str]]] = None
    example_imgs: ty.List[ty.Union[pathlib.Path, str]] = dataclasses.field(
        default_factory=tuple
    )
    parameters_description: ty.Dict[str, str] = dataclasses.field(
        default_factory=dict
    )
    argline: ty.Optional[str] = None

    def __post_init__(self) -> None:
        self.on_help = self.on_help or self.on_help_default
        event_types = ["message_new"]
        if self.allow_editing:
            event_types.append("message_edit")
        prefixes_string = f"(?:{'|'.join(self.prefixes)})"
        names_string = f"(?:{'|'.join(self.names)})"
        self._start_match_string = prefixes_string + names_string
        super().__init__(*event_types)

    def __call__(self, func: ty.Callable[..., ty.Any]) -> Command:
        self.title = self.title or func.__name__
        if not self.help_command_names:
            self.help_command_names = (self.title,)
        help_prefixes_string = f"(?:{'|'.join(self.help_prefixes)})"
        help_names_string = rf"(?:{'|'.join(self.help_names)})\s+"
        help_command_names_string = f"(?:{'|'.join(self.help_command_names)})"
        self._start_help_match_string = (
            help_prefixes_string
            + help_names_string
            + help_command_names_string
        )
        self.description = (
            self.description
            or inspect.getdoc(func)
            or "Описание отсутствует."
        )

        super().__call__(func)

        self.text_arguments = {}
        self.payload_arguments = {}

        for name, value in self._func_parameters.items():
            if isinstance(value, text_argument.TextArgument):
                self.text_arguments[name] = value
            elif isinstance(value, payload_argument.PayloadArgument):
                self.payload_arguments[name] = value
            else:
                raise AssertionError(value)  # TODO

        self.full_parameters_description = self.parameters_description.copy()
        for name, value in self.text_arguments.items():
            self.full_parameters_description.setdefault(
                name, value.description
            )

        return self

    async def handle_event(
        self, event: event_.Event
    ) -> handling_info.HandlingInfo:
        """
        Вызывается для обработки событий
        """
        # Тип события соответствует допутимым событям
        if event.type in self.event_types or not self.event_types:
            # Для help-команды # TODO: refactor
            is_start_help_matched = self._is_correct_command(
                self._start_help_match_string, event
            )
            if is_start_help_matched:
                asyncio.create_task(
                    self.answer(
                        event=event,
                        data=await utils.sync_async_run(self.on_help(event)),
                    )
                )
                return {}
            # Основная информация о процессе валидации.
            # В оптимизированной обработке отсутствует
            handled_info = handling_info.HandlingInfo(
                filters_state={},
                arguments={},
                handler_decision=(True, "Passed"),  # TODO
            )
            # TODO
            is_start_matched = self._is_correct_command(
                self._start_match_string, event
            )
            if not is_start_matched:
                return {}
            else:
                argument_string = event.get_message_object().text[
                    is_start_matched.end() :
                ]

            async for decision in self._run_through_filters(event):
                # decision[0] -- имя фильтра
                # decision[1] -- (решение фильтра, причина решения)
                handled_info["filters_state"][decision[0]] = decision[1]
                if not decision[1][0]:  # Фильтр не пройден
                    return handled_info

            # Аргументы, передаваемые в указанный обработчик из `__call__`
            arguments: ty.Dict[str, ty.Any] = {}
            handled_info["arguments"] = arguments

            async for key, value in self._init_func_arguments(
                event, argument_string
            ):
                arguments[key] = value
                if value is text_argument.PacifierArgument:
                    if key in self.on_invalid_parameter:
                        data = await utils.sync_async_run(
                            self.on_invalid_parameter[key](event)
                        )
                        asyncio.create_task(
                            self.answer(event=event, data=data)
                        )
                    return {}

            response = await utils.sync_async_run(self.func(**arguments))
            asyncio.create_task(self.answer(event=event, data=response))
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
        и переданных аргументах
        """
        if event.type in self.event_types or not self.event_types:
            async for decision in self._run_through_filters(event):
                if not decision[0][0]:  # Фильтр не пройден
                    return

        is_start_matched = self._is_correct_command(event)
        if not self._is_correct_command(event):
            return
        argument_string = event.get_message_object().text[
            is_start_matched.end() :
        ]

        # Аргументы, передаваемые в указанный обработчик из `__call__`
        arguments: ty.Dict[str, ty.Any] = {}

        async for key, value in self._init_func_arguments(
            event, argument_string
        ):
            if value is text_argument.PacifierArgument:
                if key in self.on_invalid_parameter:
                    data = await utils.sync_async_run(
                        self.on_invalid_parameter[key](event)
                    )
                    asyncio.create_task(self.answer(event=event, data=data))
                return
            else:
                arguments[key] = value

        asyncio.create_task(utils.sync_async_run(self.func(**arguments)))

    def _is_correct_command(
        self, pattern: str, event: event_.Event
    ) -> ty.Match:
        """
        Проверяет, подходит ли команда по префиксу и имени
        """
        parsed_string = event.get_message_object().text
        flags = 0 if self.case_sensitive else re.IGNORECASE
        is_matched = re.match(pattern, parsed_string, flags=flags)
        return is_matched

    @staticmethod
    async def answer(
        event: event_.Event, data: ty.Union[str, message.Message]
    ) -> None:
        """
        Быстрая отправка сообщений
        """
        if isinstance(data, message.Message):
            asyncio.create_task(data.send(event))
        else:
            asyncio.create_task(
                current.api.messages.send(
                    peer_id=event.object.message.peer_id,
                    random_id=0,
                    message=str(data),
                )
            )

    async def _init_func_arguments(  # noqa
        self, event: event_.Event, parsed_string: str
    ) -> ty.AsyncGenerator[ty.Tuple[str, ty.Any], None, None]:
        """
        Собирает аргументы для функции, основываясь на тайпингах.
        Yield'ит имя аргумента и его значение
        """

        # TextArguments
        for name, value in self.text_arguments.items():
            captured_value, parsed_string = await utils.sync_async_run(
                value.cut_part(parsed_string)
            )
            yield name, captured_value

        # PayloadArguments
        async for arguments_info in super()._init_func_arguments(
            event, self.payload_arguments
        ):
            yield arguments_info

    def on_help_default(self, _: event_.Event) -> str:
        """
        Help-обработчик по умолчанию
        """
        prefixes = ", ".join(map(lambda x: f"[id0|{x}]", self.prefixes))
        names = ", ".join(map(lambda x: f"[id0|{x}]", self.names))
        params_description = "\n".join(
            f"[id0|{pos + 1})] {info}"
            for pos, info in enumerate(self.full_parameters_description.values())
        )
        text = (
            f"Команда `{self.title}`\n\n"
            f"{self.description}\n\n"
            "Использование:\n"
            f"-> Префиксы: {prefixes or 'Отсутствуют'}\n"
            f"-> Имена: {names or 'Отстутсвуют'}\n"
            f"-> Аргументы:\n{params_description or 'Отсутствуют'}"
        )
        # TODO
        return text
