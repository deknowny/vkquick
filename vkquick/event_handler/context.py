from __future__ import annotations

import dataclasses
import typing as ty

if ty.TYPE_CHECKING:
    from vkquick.api import API
    from vkquick.bot import EventProcessingContext
    from vkquick.event import Event
    from vkquick.event_handler.handler import EventHandler
    from vkquick.event_handler.statuses import EventHandlingStatus, StatusPayload


@dataclasses.dataclass
class EventHandlingContext:
    epctx: EventProcessingContext
    event_handler: EventHandler
    handling_status: ty.Optional[EventHandlingStatus] = None
    handling_payload: ty.Optional[StatusPayload] = None
    handler_arguments: dict = dataclasses.field(default_factory=dict)
    extra: dict = dataclasses.field(default_factory=dict)

    @property
    def api(self) -> API:
        return self.epctx.bot.api

    @property
    def event(self) -> Event:
        return self.epctx.event
