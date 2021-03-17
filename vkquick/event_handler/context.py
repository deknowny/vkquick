from __future__ import annotations

import dataclasses
import typing as ty

if ty.TYPE_CHECKING:
    from vkquick.bot import EventProcessingContext
    from vkquick.event_handler.statuses import EventHandlingStatus, StatusPayload


@dataclasses.dataclass
class EventHandlingContext:
    epctx: EventProcessingContext
    handling_status: ty.Optional[EventHandlingStatus] = None
    handling_payload: ty.Optional[StatusPayload] = None
    handler_arguments: dict = dataclasses.field(default_factory=dict)
    extra: dict = dataclasses.field(default_factory=dict)
