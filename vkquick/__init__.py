try:
    # ^= 3.8
    import importlib.metadata as metadata
except ImportError:
    import importlib as metadata

# Chatbot

from vkquick.ext.chatbot.providers.attachment import (
    DocumentProvider,
    PhotoProvider,
)
from vkquick.ext.chatbot.provider.base import Provider
from vkquick.ext.chatbot.providers.message import (
    AnyMessageProvider,
    MessageProvider,
    TruncatedMessageProvider,
)
from vkquick.ext.chatbot.providers.page import (
    GroupProvider,
    PageProvider,
    UserProvider,
)
from vkquick.ext.chatbot.ui_builders.base import UIBuilder
from vkquick.ext.chatbot.ui_builders.button import Button, InitializedButton
from vkquick.ext.chatbot.ui_builders.carousel import Carousel, Element
from vkquick.ext.chatbot.ui_builders.keyboard import Keyboard
from vkquick.ext.chatbot.wrappers.attachment import (
    Attachment,
    Document,
    Photo,
)
from vkquick.ext.chatbot.wrapper.base import Wrapper
from vkquick.ext.chatbot.wrappers.message import Message, TruncatedMessage
from vkquick.ext.chatbot.wrappers.page import Group, Page, User

# Main core
from .api import API, TokenOwnerEntity, TokenOwnerType
from .bases.api_serializable import APISerializableMixin
from .bases.easy_decorator import EasyDecorator
from .bases.event import BaseEvent
from .bases.filter import Filter

# from .bot import Bot, EventProcessingContext
from .cached_property import cached_property
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

__version__ = metadata.version(__name__)
