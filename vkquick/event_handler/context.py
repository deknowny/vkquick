import dataclasses
import typing as ty

from vkquick.bot import Bot, EventProcessingContext
from vkquick.bases.event import Event
from vkquick.event_handler.statuses import EventHandlingStatus, StatusPayload


@dataclasses.dataclass
class EventHandlingContext:
    epctx: EventProcessingContext
    handling_status: ty.Optional[EventHandlingStatus] = None
    handling_payload: ty.Optional[StatusPayload] = None
    handler_arguments: dict = dataclasses.field(default_factory=dict)
    extra: dict = dataclasses.field(default_factory=dict)