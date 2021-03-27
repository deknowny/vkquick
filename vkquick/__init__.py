try:
    # ^= 3.8
    import importlib.metadata as metadata
except ImportError:
    import importlib as metadata

from .api import API, TokenOwnerEntity, TokenOwnerType
from .bases.api_serializable import APISerializableMixin
from .bases.easy_decorator import EasyDecorator
from .bases.event import Event
from .bases.events_factories import (
    EventsCallback,
    EventsFactory,
    LongPollBase,
)
from .bases.filter import Filter
from .bases.json_parser import JSONParser
from .bases.session_container import SessionContainerMixin
from .bot import Bot, EventProcessingContext
from .event import GroupEvent, UserEvent
from .event_handler.context import EventHandlingContext
from .event_handler.handler import EventHandler
from .event_handler.statuses import (
    CalledHandlerSuccessfully,
    EventHandlingStatus,
    FilterFailed,
    IncorrectEventType,
    StatusPayload,
    UnexpectedErrorOccurred,
)
from .exceptions import (
    FilterFailedError,
    NotCompatibleFilterError,
    VKAPIError,
)
from .json_parsers import (
    BuiltinJsonParser,
    OrjsonParser,
    UjsonParser,
    json_parser_policy,
)
from .longpoll import GroupLongPoll, UserLongPoll
from .pretty_view import pretty_view
from .signal import SignalHandler
from .sync_async import OptionalAwaitable, sync_async_run

__version__ = metadata.version(__name__)
