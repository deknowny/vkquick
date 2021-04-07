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
    NotCompatibleFilterError,
    StopHandlingEvent,
)


class EventHandler(EasyDecorator):
    """ """

    context_factory: ty.Type[EventHandlingContext] = EventHandlingContext

    def __init__(
        self,
        __handler: ty.Optional[ty.Callable[..., ty.Awaitable]] = None,
        *,
        handling_event_types: ty.Union[ty.Set[str], ty.Type[...]] = None,
        filters: ty.List[Filter] = None,
    ):
        self._handler = __handler
        self._handling_event_types = handling_event_types or {
            __handler.__name__
        }
        self._filters = filters or []

    @property
    def handler(self):
        return self._handler

    def is_handling_event_type(self, event_type: ty.Union[str]) -> bool:
        """

        Args:
          event_type: ty.Union[str]:
          event_type: ty.Union[str]:

        Returns:

        """
        return (
            not self._handling_event_types
            or event_type in self._handling_event_types
        )

    def add_filter(self, filter: Filter) -> EventHandler:
        """

        Args:
          filter: Filter:
          filter: Filter:

        Returns:

        """
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

    async def _run_through_filters(self, ehctx: EventHandlingContext) -> None:
        for filter_ in self._filters:
            try:
                await filter_.make_decision(ehctx)
            except FilterFailedError as error:
                ehctx.handling_status = EventHandlingStatus.FILTER_FAILED
                ehctx.handling_payload = FilterFailed(
                    filter=filter_, raised_error=error
                )
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

        await self._run_through_filters(ehctx)
        await self._prepare_handler_for_call(ehctx)

    async def _prepare_handler_for_call(
        self, ehctx: EventHandlingContext
    ) -> None:
        handler_args = self._init_handler_args(ehctx)
        handler_kwargs = self._init_handler_kwargs(ehctx)
        returned_value = await self._call_handler(ehctx, handler_args, handler_kwargs)
        raise StopHandlingEvent(
            status=EventHandlingStatus.CALLED_HANDLER_SUCCESSFULLY,
            payload=CalledHandlerSuccessfully(
                handler_returned_value=returned_value
            ),
        )

    async def _call_handler(self, ehctx: EventHandlingContext, args, kwargs) -> ty.Any:
        baked_call = self._handler(*args, **kwargs)
        returned_value = await baked_call
        return returned_value

    def _init_handler_kwargs(self, ehctx: EventHandlingContext) -> ty.Mapping:
        return {}

    def _init_handler_args(self, ehctx: EventHandlingContext) -> ty.Sequence:
        return (ehctx,)

    def __repr__(self):
        return (
            f"<vkquick.{self.__class__.__name__} handler_name={self._handler.__name__!r}>"
        )
