from __future__ import annotations
import typing as ty

from loguru import logger

from vkquick.bot import EventProcessingContext
from vkquick.bases.easy_decorator import EasyDecorator
from vkquick.bases.filter import Filter
from vkquick.exceptions import FilterFailedError, NotCompatibleFilterError
from vkquick.event_handler.context import EventHandlingContext
from vkquick.event_handler.statuses import (
    EventHandlingStatus,
    IncorrectEventType,
    FilterFailed,
    ErrorRaisedByHandlerCall,
    UnexpectedErrorOccurred,
    CalledHandlerSuccessfully,
    ErrorRaisedByPostHandlingCallback,
    IncorrectPreparedArguments
)
from vkquick.sync_async import sync_async_callable, sync_async_run


class EventHandler(EasyDecorator):
    def __init__(
        self,
        __handler: ty.Optional[ty.Callable] = None,
        *,
        handling_event_types: ty.Set[str] = None,
        filters: ty.List[Filter] = None,
        post_handling_callback: ty.Optional[
            sync_async_callable([EventHandlingContext])
        ] = None,
        pass_ehctx_as_argument: bool = True
    ):
        self._handler = __handler
        self._handling_event_types = handling_event_types or {
            __handler.__name__
        }
        self._filters = filters or []
        self._post_handling_callback = post_handling_callback
        self._pass_ehctx_as_argument = pass_ehctx_as_argument

    def is_handling_event_type(self, event_type: ty.Union[str]) -> bool:
        return event_type in self._handling_event_types

    def add_filter(self, filter: Filter) -> EventHandler:
        uncovered_event_types = self._handling_event_types - filter.__accepted_event_types__
        if self._handling_event_types - filter.__accepted_event_types__:
            raise NotCompatibleFilterError(
                filter=filter,
                event_handler=self,
                uncovered_event_types=uncovered_event_types
            )
        self._filters.append(filter)
        return self

    @logger.catch
    async def __call__(
        self, epctx: EventProcessingContext
    ) -> EventHandlingContext:
        ehctx = EventHandlingContext(epctx=epctx)
        try:
            if epctx.event.type not in self._handling_event_types:
                ehctx.handling_status = EventHandlingStatus.INCORRECT_EVENT_TYPE
                ehctx.handling_payload = IncorrectEventType()
                return ehctx

            passed_all_filters = await self.run_through_filters(ehctx)
            if not passed_all_filters:
                return ehctx

            await self.call_handler(ehctx)

        except Exception as error:
            ehctx.handling_status = EventHandlingStatus.UNEXPECTED_ERROR_OCCURRED
            ehctx.handling_payload = UnexpectedErrorOccurred(raised_error=error)
            raise error
        finally:
            try:
                if self._post_handling_callback is not None:
                    await sync_async_run(
                        self._post_handling_callback(ehctx)
                    )
            except Exception as error:
                ehctx.handling_status = EventHandlingStatus.CALLED_HANDLER_SUCCESSFULLY
                ehctx.handling_payload = ErrorRaisedByPostHandlingCallback(raised_error=error)
                raise error
            finally:
                return ehctx

    async def run_through_filters(self, ehctx: EventHandlingContext) -> bool:
        for filter_ in self._filters:
            try:
                await sync_async_run(filter_.make_decision(ehctx))
            except FilterFailedError as error:
                ehctx.handling_status = EventHandlingStatus.FILTER_FAILED
                ehctx.handling_payload = FilterFailed(filter=filter_, raised_error=error)
                await sync_async_run(filter_.handle_exception(ehctx))
                return False

        return True

    async def call_handler(self, ehctx: EventHandlingContext) -> None:
        try:
            try:
                if self._pass_ehctx_as_argument:
                    ehctx.handler_arguments["ehctx"] = ehctx
                handler_call = self._handler(**ehctx.handler_arguments)
            except TypeError as error:
                # TypeError может быть вызван и по другим причинам,
                # поэтому рекомендую использовать только корутины
                ehctx.handling_status = EventHandlingStatus.INCORRECT_PREPARED_ARGUMENTS
                ehctx.handling_payload = IncorrectPreparedArguments(raised_error=error)
                raise error
            else:
                returned_value = await sync_async_run(handler_call)
        except Exception as error:
            ehctx.handling_status = EventHandlingStatus.ERROR_RAISED_BY_HANDLER_CALL
            ehctx.handling_payload = ErrorRaisedByHandlerCall(raised_error=error)
            raise error
        else:
            ehctx.handling_status = EventHandlingStatus.CALLED_HANDLER_SUCCESSFULLY
            ehctx.handling_payload = CalledHandlerSuccessfully(handler_returned_value=returned_value)
