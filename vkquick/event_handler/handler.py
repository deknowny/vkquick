from __future__ import annotations

import inspect
import typing as ty

from loguru import logger

from vkquick.bases.easy_decorator import EasyDecorator
from vkquick.bases.filter import Filter
from vkquick.event_handler.context import EventHandlingContext
from vkquick.event_handler.statuses import (
    CalledHandlerSuccessfully,
    EventHandlingStatus,
    FilterFailed,
    IncorrectEventType,
    UnexpectedErrorOccurred,
)
from vkquick.exceptions import (
    FilterFailedError,
    IncorrectPreparedArgumentsError,
    NotCompatibleFilterError,
    StopHandlingEvent,
)
from vkquick.sync_async import sync_async_run


class EventHandler(EasyDecorator):
    def __init__(
        self,
        __handler: ty.Optional[ty.Callable] = None,
        *,
        handling_event_types: ty.Union[ty.Set[str], ty.Type[...]] = None,
        filters: ty.List[Filter] = None,
        pass_ehctx_as_argument: bool = True,
    ):
        self._handler = __handler
        self._handling_event_types = handling_event_types or {
            __handler.__name__
        }
        self._filters = filters or []
        self._pass_ehctx_as_argument = pass_ehctx_as_argument
        self._available_arguments_name = frozenset(
            inspect.signature(self._handler).parameters.keys()
        )

    def is_handling_event_type(self, event_type: ty.Union[str]) -> bool:
        return (
            self._handling_event_types is ...
            or event_type in self._handling_event_types
        )

    def add_filter(self, filter: Filter) -> EventHandler:
        if filter.__accepted_event_types__ is not ...:
            uncovered_event_types = (
                self._handling_event_types - filter.__accepted_event_types__
            )
            if self._handling_event_types - filter.__accepted_event_types__:
                raise NotCompatibleFilterError(
                    filter=filter,
                    event_handler=self,
                    uncovered_event_types=uncovered_event_types,
                )
        self._filters.append(filter)
        return self

    @logger.catch
    async def __call__(self, ehctx: EventHandlingContext) -> None:
        try:
            await self._handle_event(ehctx)
        except StopHandlingEvent as handling_info:
            ehctx.handling_status = handling_info.status
            ehctx.handling_payload = handling_info.payload
        except Exception as error:
            ehctx.handling_status = (
                EventHandlingStatus.UNEXPECTED_ERROR_OCCURRED
            )
            ehctx.handling_payload = UnexpectedErrorOccurred(
                raised_error=error
            )
            raise error

    async def run_through_filters(self, ehctx: EventHandlingContext) -> None:
        for filter_ in self._filters:
            try:
                await sync_async_run(filter_.make_decision(ehctx))
            except FilterFailedError as error:
                ehctx.handling_status = EventHandlingStatus.FILTER_FAILED
                ehctx.handling_payload = FilterFailed(
                    filter=filter_, raised_error=error
                )
                await sync_async_run(filter_.handle_exception(ehctx))
                raise StopHandlingEvent(
                    status=EventHandlingStatus.FILTER_FAILED,
                    payload=FilterFailed(filter=filter_, raised_error=error),
                ) from error

    async def _handle_event(self, ehctx: EventHandlingContext) -> None:
        if ehctx.epctx.event.type not in self._handling_event_types:
            raise StopHandlingEvent(
                status=EventHandlingStatus.INCORRECT_EVENT_TYPE,
                payload=IncorrectEventType(),
            )

        await self.run_through_filters(ehctx)
        self._processing_passed_arguments(ehctx)
        await self.call_handler(ehctx)

    async def call_handler(self, ehctx: EventHandlingContext):
        baked_call = self._handler(**ehctx.handler_arguments)
        returned_value = await sync_async_run(baked_call)
        raise StopHandlingEvent(
            status=EventHandlingStatus.CALLED_HANDLER_SUCCESSFULLY,
            payload=CalledHandlerSuccessfully(
                handler_returned_value=returned_value
            ),
        )

    def _processing_passed_arguments(
        self, ehctx: EventHandlingContext
    ) -> None:
        if self._pass_ehctx_as_argument:
            ehctx.handler_arguments["ehctx"] = ehctx
        self._check_passed_arguments(ehctx)

    def _check_passed_arguments(self, ehctx: EventHandlingContext) -> None:
        passed_arguments_name = frozenset(ehctx.handler_arguments.keys())
        if passed_arguments_name != self._available_arguments_name:
            raise IncorrectPreparedArgumentsError(
                expected_names=self._available_arguments_name,
                actual_names=passed_arguments_name,
            )

    def __repr__(self):
        return (
            f"<vkquick.EventHandler handler_name={self._handler.__name__!r}>"
        )
