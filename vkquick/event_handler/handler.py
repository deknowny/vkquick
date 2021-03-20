from __future__ import annotations

import typing as ty

from loguru import logger

from vkquick.bases.easy_decorator import EasyDecorator
from vkquick.bases.filter import Filter
from vkquick.event_handler.context import EventHandlingContext
from vkquick.event_handler.statuses import (
    CalledHandlerSuccessfully,
    ErrorRaisedByHandlerCall,
    ErrorRaisedByPostHandlingCallback,
    EventHandlingStatus,
    FilterFailed,
    IncorrectEventType,
    IncorrectPreparedArguments,
    UnexpectedErrorOccurred,
)
from vkquick.exceptions import FilterFailedError, NotCompatibleFilterError
from vkquick.sync_async import sync_async_callable, sync_async_run


class EventHandler(EasyDecorator):
    def __init__(
        self,
        __handler: ty.Optional[ty.Callable] = None,
        *,
        handling_event_types: ty.Union[ty.Set[str], ty.Type[...]] = None,
        filters: ty.List[Filter] = None,
        post_handling_callbacks: ty.Optional[
            ty.List[sync_async_callable([EventHandlingContext])]
        ] = None,
        pass_ehctx_as_argument: bool = True
    ):
        self._handler = __handler
        self._handling_event_types = handling_event_types or {
            __handler.__name__
        }
        self._filters = filters or []
        self._post_handling_callbacks = post_handling_callbacks or []
        self._pass_ehctx_as_argument = pass_ehctx_as_argument

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

    async def __call__(
        self, ehctx: EventHandlingContext
    ) -> EventHandlingContext:
        try:
            await self._handle_event(ehctx)
        except Exception as error:
            ehctx.handling_status = (
                EventHandlingStatus.UNEXPECTED_ERROR_OCCURRED
            )
            ehctx.handling_payload = UnexpectedErrorOccurred(
                raised_error=error
            )
        finally:
            try:
                await self._call_post_handling_callbacks(ehctx)
            except Exception as error:
                ehctx.handling_status = (
                    EventHandlingStatus.CALLED_HANDLER_SUCCESSFULLY
                )
                ehctx.handling_payload = ErrorRaisedByPostHandlingCallback(
                    raised_error=error
                )
            finally:
                return ehctx

    async def run_through_filters(self, ehctx: EventHandlingContext) -> bool:
        for filter_ in self._filters:
            try:
                await sync_async_run(filter_.make_decision(ehctx))
            except FilterFailedError as error:
                ehctx.handling_status = EventHandlingStatus.FILTER_FAILED
                ehctx.handling_payload = FilterFailed(
                    filter=filter_, raised_error=error
                )
                await sync_async_run(filter_.handle_exception(ehctx))
                return False

        return True

    @logger.catch(reraise=True)
    async def _call_post_handling_callbacks(
        self, ehctx: EventHandlingContext
    ) -> None:
        for callback in self._post_handling_callbacks:
            await sync_async_run(callback(ehctx))

    @logger.catch(reraise=True)
    async def _handle_event(self, ehctx: EventHandlingContext) -> None:
        if ehctx.epctx.event.type not in self._handling_event_types:
            ehctx.handling_status = EventHandlingStatus.INCORRECT_EVENT_TYPE
            ehctx.handling_payload = IncorrectEventType()
            return

        passed_all_filters = await self.run_through_filters(ehctx)
        if not passed_all_filters:
            return

        await self.call_handler(ehctx)

    @logger.catch(reraise=True)
    async def call_handler(self, ehctx: EventHandlingContext) -> None:
        try:
            try:
                if self._pass_ehctx_as_argument:
                    ehctx.handler_arguments["ehctx"] = ehctx
                handler_call = self.__call_handler(ehctx)
            except TypeError as error:
                # TypeError может быть вызван и по другим причинам,
                # поэтому рекомендую использовать только корутины
                ehctx.handling_status = (
                    EventHandlingStatus.INCORRECT_PREPARED_ARGUMENTS
                )
                ehctx.handling_payload = IncorrectPreparedArguments(
                    raised_error=error
                )
                return
            else:
                returned_value = await self.__await_handler(handler_call)
        except Exception as error:
            ehctx.handling_status = (
                EventHandlingStatus.ERROR_RAISED_BY_HANDLER_CALL
            )
            ehctx.handling_payload = ErrorRaisedByHandlerCall(
                raised_error=error
            )
        else:
            ehctx.handling_status = (
                EventHandlingStatus.CALLED_HANDLER_SUCCESSFULLY
            )
            ehctx.handling_payload = CalledHandlerSuccessfully(
                handler_returned_value=returned_value
            )

    @logger.catch(reraise=True)
    def __call_handler(self, ehctx: EventHandlingContext):
        return self._handler(**ehctx.handler_arguments)

    @logger.catch(reraise=True)
    async def __await_handler(self, handler_call):
        return await sync_async_run(handler_call)
