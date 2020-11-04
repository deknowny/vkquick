from __future__ import annotations
import re
import time
import inspect
import typing as ty

from vkquick.utils import AttrDict, sync_async_run, sync_async_callable
from vkquick.context import Context
from vkquick.base.debugger import HandlingStatus
from vkquick.base.filter import Filter, Decision
from vkquick.events_generators.event import Event
from vkquick.argument import Argument
from vkquick.base.text_cutter import TextCutter, UnmatchedArgument


class Command(Filter):
    def __init__(
        self,
        *,
        prefixes: ty.Iterable[str] = (),
        names: ty.Iterable[str] = (),
        description: ty.Optional[str] = None,
        routing_command_re_flags: re.RegexFlag = re.IGNORECASE,
        extra: ty.Optional[dict] = None,
    ):
        self._prefixes = tuple(prefixes)
        self._names = tuple(names)
        self._description = description
        self._routing_command_re_flags = routing_command_re_flags
        self._extra = AttrDict(extra or {})

        self._filters: ty.List[Filter] = [self]
        self._reaction_arguments: ty.List[ty.Tuple[str, ty.Any]] = []
        self._reaction_context_argument_name = None

    @property
    def extra(self) -> AttrDict:
        """
        Extra values
        """
        return self._extra

    @property
    def prefixes(self) -> ty.Tuple[str]:
        return self._prefixes

    @prefixes.setter
    def prefixes(self, value: ty.Iterable[str]) -> None:
        self._prefixes = tuple(value)
        self._build_routing_regex()

    @property
    def names(self) -> ty.Tuple[str]:
        return self._names

    @names.setter
    def names(self, value: ty.Iterable[str]) -> None:
        self._prefixes = tuple(value)
        self._build_routing_regex()

    def __call__(self, reaction: sync_async_callable(..., None)):
        self.reaction = reaction
        self._resolve_arguments()

    async def handle_event(self, event: Event):
        start_handling_stamp = time.monotonic()
        context = Context(
            message=event.message.object, client_info=event.client_info
        )
        (
            passed_every_filter,
            filters_decision,
        ) = await self.run_through_filters(context)
        if not passed_every_filter:
            end_handling_stamp = time.monotonic()
            taken_time = end_handling_stamp - start_handling_stamp
            return HandlingStatus(
                all_filters_passed=False, taken_time=taken_time
            )

        await self.call_reaction(context)

        end_handling_stamp = time.monotonic()
        taken_time = end_handling_stamp - start_handling_stamp

        return HandlingStatus(
            all_filters_passed=True,
            passed_arguments=context.extra.reaction_arguments,
            taken_time=taken_time,
        )

    async def run_through_filters(
        self, context: Context
    ) -> ty.Tuple[bool, ty.List[HandlingStatus]]:
        decisions = []
        for filter_ in self._filters:
            decision = await filter_.make_decision(context)
            decisions.append(decision)
            if not decision.passed:
                return False, decisions

        return True, decisions

    def on_invalid_filter(self, filter_: Filter, /):
        ...

    def on_invalid_argument(self, name: str):
        ...

    async def make_decision(self, context: Context):
        matched = self._command_routing_regex.match(
            context.message.text
        )
        if matched:
            arguments_string = context.message.text[matched.end():]
        else:
            return Decision(
                False,
                f"Команда не подходит под шаблон `{self._command_routing_regex}`"
            )

        is_parsed, arguments = self.init_text_arguments(arguments_string, context)

        if not is_parsed:
            unparsed_argument_name, _ = arguments.popitem()
            return Decision(
                False,
                f"Не удалось выявить значение для аргумента `{unparsed_argument_name}`"
            )
        # TODO

    async def init_text_arguments(self, arguments_string: str, context: Context) -> ty.Tuple[bool, dict]:
        arguments = {}
        if self._reaction_context_argument_name is not None:
            arguments[self._reaction_context_argument_name] = context

        new_arguments_string = arguments_string
        for name, cutter in self._reaction_arguments:
            parsed_value, new_arguments_string = await sync_async_run(
                cutter.cut_part(arguments_string)
            )
            arguments[name] = parsed_value
            if parsed_value is UnmatchedArgument:
                return False, arguments

        if new_arguments_string:
            return False, arguments
        return True, arguments



    async def call_reaction(self, context: Context) -> None:
        result = self.reaction(**context.extra.reaction_arguments)
        result = await sync_async_run(result)
        if result is not None:
            await context.message.reply(message=result)

    def _resolve_arguments(self):
        parameters = inspect.signature(self.reaction).parameters
        parameters = list(parameters.items())
        seems_context, *cutters = parameters

        # def foo(ctx: Context): ...
        # def foo(ctx=Context)
        # def foo(ctx): ...
        if (
            seems_context[1].annotation is Context
            or seems_context[1].default is Context
            or (
                seems_context[1].annotation is seems_context[1].empty
                and seems_context[1].default is seems_context[1].empty
            )
        ):
            self._reaction_context_argument_name[
                seems_context[0]  # black: ignore
            ] = seems_context[1].annotation
        else:
            self._resolve_text_cutter(seems_context)

        for argument in cutters:
            self._resolve_text_cutter(argument)

    def _resolve_text_cutter(
        self, argument: ty.Tuple[str, inspect.Parameter]
    ):
        # def foo(arg: int = vq.Integer()): ...
        # def foo(arg: vq.Integer()): ...
        # def foo(arg: int = vq.Integer): ...
        # def foo(arg: vq.Integer): ...
        name, value = argument
        if value.default != value.empty:
            cutter = value.default
        elif value.annotation != value.empty:
            cutter = value.annotation
        else:
            raise TypeError()  # TODO

        if inspect.isclass(value) and issubclass(cutter, TextCutter):
            real_type = cutter()
        elif isinstance(cutter, TextCutter):
            real_type = cutter
        else:
            raise TypeError()  # TODO

        self._reaction_arguments.append((name, real_type))

    def _build_routing_regex(self):
        self._prefixes_regex = "|".join(self._prefixes)
        self._names_regex = "|".join(self._names)
        if len(self._prefixes) > 1:
            self.prefixes_regex = f"(?:{self._prefixes_regex})"
        if len(self._names) > 1:
            self._names_regex = f"(?:{self._names_regex})"
        self._command_routing_regex = re.compile(
            self._prefixes_regex + self._names_regex,
            flags=self._routing_command_re_flags,
        )
