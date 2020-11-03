from __future__ import annotations
import re
import time
import inspect
import typing as ty

from vkquick.utils import AttrDict, sync_async_run, sync_async_callable
from vkquick.context import Context
from vkquick.base.debugger import HandlingStatus
from vkquick.base.filter import Filter
from vkquick.events_generators.event import Event
from vkquick.argument import Argument


class Command(Filter):
    def __init__(
        self, *,
        prefixes: ty.Collection[str] = (),
        names: ty.Collection[str] = (),
        description: ty.Optional[str] = None,
        routing_command_re_flags: re.RegexFlag = re.IGNORECASE,
        extra: ty.Optional[dict] = None
    ):
        self._prefixes = tuple(prefixes)
        self._names = tuple(names)
        self._description = description
        self._routing_command_re_flags = routing_command_re_flags
        self._extra = AttrDict(extra or {})

        self._filters: ty.List[Filter] = [self]

    @property
    def extra(self) -> AttrDict:
        """
        Extra values
        """
        return self._extra

    @property
    def prefixes(self) -> ty.Tuple[str]:
        return self._prefixes

    @property
    def names(self) -> ty.Tuple[str]:
        return self._names

    def __call__(self, reaction: sync_async_callable(..., None)):
        self.reaction = reaction
        self._resolve_arguments()

    async def handle_event(self, event: Event):
        start_handling_stamp = time.monotonic()
        context = Context(
            message=event.message.object,
            client_info=event.client_info
        )
        passed_every_filter, filters_decision = await self.run_through_filters(context)
        if not passed_every_filter:
            end_handling_stamp = time.monotonic()
            taken_time = end_handling_stamp - start_handling_stamp
            return HandlingStatus(
                all_filters_passed=False,
                taken_time=taken_time
            )

        result = self.reaction(**context.extra.reaction_arguments)
        await sync_async_run(result)

        end_handling_stamp = time.monotonic()
        taken_time = end_handling_stamp - start_handling_stamp

        return HandlingStatus(
            all_filters_passed=True,
            passed_arguments=context.extra.reaction_arguments,
            taken_time=taken_time
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
        ...

    def _resolve_arguments(self):
        parameters = inspect.signature(self.reaction).parameters
        for name, value in parameters.items():
            if value.annotation != value.empty and


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























