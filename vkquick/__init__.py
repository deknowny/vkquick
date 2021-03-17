import importlib.metadata

from .api import API, TokenOwnerEntity, TokenOwnerType
from .bot import Bot, EventProcessingContext
from .event import GroupEvent, UserEvent
from .exceptions import (
    VKAPIError,
    FilterFailedError,
    NotCompatibleFilterError,
)
from .json_parsers import (
    BuiltinJsonParser,
    OrjsonParser,
    UjsonParser,
    json_parser_policy,
)
from .longpoll import UserLongPoll, GroupLongPoll
from .signal_handler import SignalHandler
from .sync_async import sync_async_callable, sync_async_run

from .event_handler.handler import EventHandler
from .event_handler.statuses import (
    EventHandlingStatus,
    StatusPayload,
    IncorrectEventType,
    IncorrectPreparedArguments,
    ErrorRaisedByPostHandlingCallback,
    CalledHandlerSuccessfully,
    ErrorRaisedByHandlerCall,
    FilterFailed,
    UnexpectedErrorOccurred,
)
from .event_handler.context import EventHandlingContext

from .bases.api_serializable import APISerializableMixin
from .bases.easy_decorator import EasyDecorator
from .bases.event import Event
from .bases.events_factories import (
    EventsFactory,
    EventsCallback,
    LongPollBase,
)
from .bases.filter import Filter
from .bases.json_parser import JSONParser
from .bases.session_container import SessionContainerMixin


__version__ = importlib.metadata.version(__name__)
del importlib.metadata
