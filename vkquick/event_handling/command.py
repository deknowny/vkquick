import asyncio
import enum
import inspect
import re
import typing as ty

import vkquick.event_handling.event_handler
import vkquick.event_handling.message
import vkquick.events_generators.event
import vkquick.base.payload_argument
import vkquick.base.text_argument
import vkquick.base.filter
import vkquick.utils


Response = ty.Union[str, vkquick.event_handling.message.Message]


class CommandTextStatus(vkquick.base.filter.DecisionStatus):
    NOT_ROUTED = enum.auto()
    EXCESS_ARGUMENT = enum.auto()
    NOT_CAPTURED_ARGUMENT = enum.auto()
    PASSED = enum.auto()


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
                vkquick.utils.sync_async_callable(
                    [str, int, str, vkquick.events_generators.event.Event],
                    Response,
                ),
            ]
        ] = None,
        matching_command_routing_re_flags: re.RegexFlag = re.IGNORECASE,
        on_filters_decision: ty.Optional[
            ty.Dict[
                vkquick.base.filter.DecisionStatus,
                vkquick.utils.sync_async_callable(
                    [
                        vkquick.events_generators.event.Event,
                        vkquick.utils.AttrDict,
                    ],
                    Response,
                ),
            ]
        ] = None,
        help_reaction: ty.Optional[
            ty.Callable[
                [vkquick.events_generators.event.Event],
                vkquick.utils.sync_async_callable(
                    [vkquick.events_generators.event.Event], Response
                ),
            ]
        ] = None,
        ignore_editing: bool = False,
    ):
        self.on_invalid_text_argument = on_invalid_text_argument or {}
        self.on_filters_decision = on_filters_decision or {}
        self._made_text_arguments = {}

        self.origin_prefixes = tuple(prefixes)
        self.origin_names = tuple(names)
        self.title = title
        self.description = description
        self.help_reaction = help_reaction

        self.prefixes = "|".join(self.origin_prefixes)
        self.names = "|".join(self.origin_names)
        if len(self.origin_prefixes) > 1:
            self.prefixes = f"(?:{self.prefixes})"
        if len(self.origin_names) > 1:
            self.names = f"(?:{self.names})"
        self.command_routing_regex = re.compile(
            self.prefixes + self.names,
            flags=matching_command_routing_re_flags,
        )

        self.text_arguments = {}

        handled_event_types = ["message_new", 4]
        if not ignore_editing:
            handled_event_types.extend("message_edit")
        super().__init__(*handled_event_types)

    def __call__(
        self, reaction: vkquick.utils.sync_async_callable(..., Response)
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
        for name, value in self.reaction_arguments.items():
            if isinstance(value, vkquick.base.text_argument.TextArgument,):
                self.text_arguments[name] = value
            elif isinstance(
                value, vkquick.base.payload_argument.PayloadArgument,
            ):
                self.payload_arguments[name] = value
                # TODO: TypeError in other method

    async def command_text_filter(
        self, event: vkquick.events_generators.event.Event
    ) -> vkquick.base.filter.FilterResponse:
        matched, arguments_string = self.matching_command_routing(
            event.get_message_object().text
        )
        if not matched:
            decision = vkquick.base.filter.Decision(
                False,
                f"Вызванная команда не совпадает с шаблоном `{self.command_routing_regex.pattern}`",
            )
            response = vkquick.base.filter.FilterResponse(
                CommandTextStatus.NOT_ROUTED, decision
            )
            return response

        # arguments_string -- остаток от текста, откуда вырезались аргументы
        # text_arguments -- словарь с инстансами `TextArguments`
        matched, arguments_string, text_arguments = await self.cut_arguments(
            event, arguments_string
        )
        if not matched:
            if arguments_string:
                decision = vkquick.base.filter.Decision(
                    False,
                    f"Передано излишнее значение `{arguments_string}`, на которое не обозначены аргументы",
                )
                response = vkquick.base.filter.FilterResponse(
                    CommandTextStatus.EXCESS_ARGUMENT, decision
                )
                return response

            unmatched_argument_name = list(text_arguments)[-1]
            decision = vkquick.base.filter.Decision(
                False,
                f"Аргумент `{unmatched_argument_name}` не вырезан из строки `{arguments_string}`",
            )
            response = vkquick.base.filter.FilterResponse(
                CommandTextStatus.NOT_CAPTURED_ARGUMENT, decision
            )
            return response

        self._made_text_arguments[event.event_id] = text_arguments
        decision = vkquick.base.filter.Decision(
            True, "Текст команды подходит под шаблон"
        )
        response = vkquick.base.filter.FilterResponse(
            CommandTextStatus.PASSED, decision
        )
        return response

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
            if arguments_string.lstrip() == arguments_string and arguments_string:
                return False, arguments_string
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
            if matched_value is vkquick.base.text_argument.UnmatchedArgument:
                asyncio.create_task(
                    self._on_unsuccessful_cutting(
                        name, arguments_string, value, event
                    )
                )
                return False, arguments_string, text_arguments

        if arguments_string:
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
        text_argument: vkquick.base.text_argument.TextArgument,
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
    ) -> ty.Tuple[
        bool, ty.List[ty.Tuple[vkquick.base.filter.FilterResponse, str]]
    ]:
        command_text_filter_decision = await self.command_text_filter(event)
        command_text_filter_name = "CommandText"
        passed_command_text_filter = (
            command_text_filter_decision.decision.passed
        )

        if not passed_command_text_filter:
            return (
                False,
                [(command_text_filter_decision, command_text_filter_name)],
            )

        filters_decision: ty.List[
            ty.Tuple[vkquick.base.filter.FilterResponse, str]
        ] = [(command_text_filter_decision, command_text_filter_name)]
        passed_all, other_filters_decision = await super().run_trough_filters(
            event
        )

        for filter_decision in other_filters_decision:
            if filter_decision[0].status_code in self.on_filters_decision:
                filter_decision_reaction = self.on_filters_decision[
                    filter_decision[0].status_code
                ]
                response = await vkquick.utils.sync_async_run(
                    filter_decision_reaction(event, filter_decision[0].extra)
                )
                await self.routing_reaction_response(response, event)

            filters_decision.append(filter_decision)

        return passed_all, filters_decision

    async def init_reaction_arguments(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Dict[str, ty.Any]:
        """
        Инициализирует значения для аргументов функции.
        `TextArgument` и `PayloadArgument` в этой реализации
        """
        payload_arguments = await super().init_reaction_arguments(event)
        text_arguments = self._made_text_arguments.pop(event.event_id)
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
        response: Response, event: vkquick.events_generators.event.Event,
    ) -> None:
        if isinstance(response, vkquick.event_handling.message.Message):
            asyncio.create_task(response.send(event))
        elif response is not None:
            message = vkquick.event_handling.message.Message(str(response))
            asyncio.create_task(message.send(event))
