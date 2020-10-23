import asyncio
import inspect
import re
import typing as ty

import vkquick.event_handling.event_handler
import vkquick.event_handling.message
import vkquick.events_generators.event
import vkquick.event_handling.reaction_argument.payload_arguments.base
import vkquick.event_handling.reaction_argument.text_arguments.base
import vkquick.event_handling.filters.base
import vkquick.utils


class Command(vkquick.event_handling.event_handler.EventHandler):
    def __init__(
        self,
        *,
        title: ty.Optional[str] = None,
        description: ty.Optional[str] = None,
        prefixes: ty.Iterable[str] = (),
        names: ty.Iterable[str] = (),
        on_invalid_text_argument: ty.Optional[
            ty.Dict[
                str,
                ty.Callable[
                    [str, int, str, vkquick.events_generators.event.Event],
                    ty.Union[
                        ty.Awaitable[
                            ty.Union[
                                str, vkquick.event_handling.message.Message
                            ]
                        ],
                        ty.Union[str, vkquick.event_handling.message.Message],
                    ],
                ],
            ]
        ] = None,
        matching_command_routing_re_flags: re.RegexFlag = re.IGNORECASE,
        on_unapproved_filter: ty.Optional[
            ty.Dict[
                vkquick.event_handling.filters.base.Filter,
                ty.Callable[
                    [vkquick.events_generators.event.Event],
                    ty.Union[
                        str,
                        vkquick.event_handling.message.Message,
                        ty.Awaitable[
                            ty.Union[
                                str, vkquick.event_handling.message.Message
                            ]
                        ],
                    ],
                ],
            ]
        ] = None,
        help_reaction: ty.Optional[
            ty.Callable[
                [vkquick.events_generators.event.Event],
                ty.Union[
                    str,
                    vkquick.event_handling.message.Message,
                    ty.Awaitable[
                        ty.Union[str, vkquick.event_handling.message.Message]
                    ],
                ],
            ]
        ] = None,
        ignore_editing: bool = False,
    ):
        self.on_invalid_text_argument = on_invalid_text_argument or {}
        self.on_unapproved_filter = on_unapproved_filter or {}
        self._made_text_arguments = {}

        self.origin_prefixes = tuple(prefixes)
        self.origin_names = tuple(names)
        self.title = title
        self.description = description
        self.help_reaction = help_reaction

        self.prefixes = "|".join(self.origin_prefixes)
        self.names = "|".join(self.origin_names)
        self.command_routing_regex = re.compile(
            f"(?:{self.prefixes})(?:{self.names})",
            flags=matching_command_routing_re_flags,
        )

        handled_event_types = ["message_new", 4]
        if not ignore_editing:
            handled_event_types.extend("message_edit")
        super().__init__(*handled_event_types)

    def __call__(
        self,
        reaction: ty.Callable[
            ...,
            ty.Union[
                ty.Awaitable[
                    ty.Union[vkquick.event_handling.message.Message, str]
                ],
                vkquick.event_handling.message.Message,
                str,
            ],
        ],
    ):
        super().__call__(reaction)
        self._separate_reaction_arguments()
        if self.title is None:
            self.title = reaction.__name__
        if self.description is None:
            self.description = inspect.getdoc(reaction)

        return self

    def _separate_reaction_arguments(self) -> None:
        """
        Разделяет `self.reaction_arguments` на `TextArgument` и `PayloadArgument`
        """
        self.payload_arguments = {}
        self.text_arguments = {}
        for name, value in self.reaction_arguments.items():
            if isinstance(
                value,
                vkquick.event_handling.reaction_argument.text_arguments.base.TextArgument,
            ):
                self.text_arguments[name] = value
            elif isinstance(
                value,
                vkquick.event_handling.reaction_argument.payload_arguments.base.PayloadArgument,
            ):
                self.payload_arguments[name] = value
                # TODO: TypeError in other method

    async def command_text_filter(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Tuple[bool, str]:
        matched, arguments_string = self.matching_command_routing(
            event.get_message_object().text
        )
        if not matched:
            return (
                False,
                f"Вызванная команда не совпадает с шаблоном `{self.command_routing_regex.pattern}`",
            )

        # arguments_string -- остаток от текста, откуда вырезались аргументы
        # text_arguments -- словарь с инстансами `TextArguments`
        matched, arguments_string, text_arguments = await self.cut_arguments(
            event, arguments_string
        )
        if not matched:
            if arguments_string:
                return (
                    False,
                    f"Передано излишнее значение `{arguments_string}`, на которое не обозначены аргументы",
                )
            unmatched_argument_name = list(text_arguments)[-1]
            return (
                False,
                f"Аргумент `{unmatched_argument_name}` не вырезан из строки `{arguments_string}`",
            )

        if isinstance(event(), list):
            event_id = event[1]
        else:
            event_id = event.event_id
        self._made_text_arguments[event_id] = text_arguments
        return True, "Текст команды подходит под шаблон"

    def matching_command_routing(
        self, command_text: str
    ) -> ty.Tuple[bool, str]:
        """
        Матчит текст команды под ее роутинг (префикс и имя).

        Возвращает кортеж из:
        * Подходит ли имя и префикс команды
        * Строку с аргументами (если команда подходит, иначе `""`)
        """
        matched = self.command_routing_regex.match(command_text)
        if matched:
            arguments_string = command_text[matched.end() :]
            return True, arguments_string
        return False, ""

    async def cut_arguments(
        self,
        event: vkquick.events_generators.event.Event,
        arguments_string: str,
    ) -> ty.Tuple[bool, str, ty.Dict[str, ty.Any]]:
        """
        Вырезает аргументы из `arguments_string`.

        Возвращает кортеж из:
        * Подходят ли все аргументы под `arguments_string`
        * Словарь, где ключ -- имя аргумента, значение -- значение
        """
        text_arguments: ty.Dict[str, ty.Any] = {}
        arguments_string = arguments_string.lstrip()
        for name, value in self.text_arguments.items():
            (
                matched_value,
                arguments_string,
            ) = await vkquick.utils.sync_async_run(
                value.cut_part(arguments_string)
            )
            text_arguments[name] = matched_value
            arguments_string = arguments_string.lstrip()
            if (
                matched_value
                is vkquick.event_handling.reaction_argument.text_arguments.base.UnmatchedArgument
            ):
                asyncio.create_task(
                    self._on_unsuccessful_cutting(
                        name, arguments_string, value, event
                    )
                )
                return False, arguments_string, text_arguments

        if arguments_string and self.text_arguments:
            asyncio.create_task(
                self._on_unsuccessful_cutting(
                    name, arguments_string, value, event
                )
            )
            return False, arguments_string, text_arguments

        return True, arguments_string, text_arguments

    async def _on_unsuccessful_cutting(
        self,
        argument_name: str,
        argument_string: str,
        text_argument: vkquick.event_handling.reaction_argument.text_arguments.base.TextArgument,
        event: vkquick.events_generators.event.Event,
    ) -> None:
        argument_position = (
            list(self.text_arguments.keys()).index(argument_name) + 1
        )
        if argument_name in self.on_invalid_text_argument:
            func_for_invalid = self.on_invalid_text_argument[argument_name]
        else:
            func_for_invalid = text_argument.invalid_value
        response = func_for_invalid(
            argument_name=argument_name,
            argument_position=argument_position,
            argument_string=argument_string,
            event=event,
        )
        asyncio.create_task(self.routing_reaction_response(response, event))

    async def run_trough_filters(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Tuple[bool, ty.List[ty.Tuple[bool, str, str]]]:
        """

        """
        passed_all, filters_decision = await super().run_trough_filters(event)
        if passed_all:
            passed_text, description_text = await self.command_text_filter(
                event
            )
            name = "CommandText"
            passed_all = passed_text
            filters_decision.append((passed_text, description_text, name))
        else:
            for (
                filter_,
                filter_reaction,
            ) in self.on_unapproved_filter.items():
                if filter_.__name__ == filters_decision[-1][2]:
                    response = await vkquick.utils.sync_async_run(
                        filter_reaction(event)
                    )
                    await self.routing_reaction_response(response, event)

        return passed_all, filters_decision

    async def init_reaction_arguments(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Dict[str, ty.Any]:
        """
        Инициализирует значения для аргументов функции.
        `TextArgument` и `PayloadArgument` в этой реализации
        """
        payload_arguments = await super().init_reaction_arguments(event)
        if isinstance(event(), list):
            event_id = event[1]
        else:
            event_id = event.event_id
        text_arguments = self._made_text_arguments.pop(event_id)
        # Reaction аргументы. Абсолютно все
        payload_arguments.update(text_arguments)
        return payload_arguments

    async def call_reaction(
        self,
        event: vkquick.events_generators.event.Event,
        arguments: ty.Dict[str, ty.Any],
    ) -> None:
        """
        Вызывает реакцию с аргументами из `arguments`.
        То, что вернула реакция, используется для отправки сообщения
        """
        response = await vkquick.utils.sync_async_run(
            self.reaction(**arguments)
        )
        asyncio.create_task(self.routing_reaction_response(response, event))

    @staticmethod
    async def routing_reaction_response(
        response: ty.Union[str, vkquick.event_handling.message.Message],
        event: vkquick.events_generators.event.Event,
    ) -> None:
        """

        """
        if isinstance(response, vkquick.event_handling.message.Message):
            asyncio.create_task(response.send(event))
        elif response is not None:
            message = vkquick.event_handling.message.Message(str(response))
            asyncio.create_task(message.send(event))

    def generate_default_help_text(self) -> str:
        prefixes = "\n".join(
            map(lambda x: f"-> [id0|{x}]", self.origin_prefixes)
        )
        names = "\n".join(map(lambda x: f"-> [id0|{x}]", self.origin_names))
        params_description = "\n".join(
            f"[id0|{pos + 1}.] {arg.usage_description()}"
            for pos, arg in enumerate(self.text_arguments.values())
        )
        description = self.description or "Описание отсутствует"
        text = (
            f"Помощь по команде `{self.title}`\n\n"
            f"{description}\n\n"
            "[Использование]\n"
            f"Возможные префиксы:\n{prefixes or '> Отсутствуют'}\n"
            f"Возможные имена:\n{names or '> Отстутсвуют'}\n"
            f"Аргументы, которые необходимо передать при вызове:\n{params_description or 'Отсутствуют'}"
        )

        return text
