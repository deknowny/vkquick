try:
    # ^= 3.8
    import importlib.metadata as metadata
except ImportError:
    import importlib as metadata

# Chatbot
import typing

from vkquick.ext.chatbot.chat_bot import ChatBot
from vkquick.ext.chatbot.command.command import Command
from vkquick.ext.chatbot.command.context import Context
from vkquick.ext.chatbot.command.statuses import (
    CommandStatus,
    IncorrectArgument,
    MissedArgument,
    NotRouted,
    UnexpectedArgument,
)
from vkquick.ext.chatbot.command.text_cutters.base import (
    Argument,
    CommandTextArgument,
    CutterParsingResponse,
    TextCutter,
    cut_part_via_regex,
)
from vkquick.ext.chatbot.command.text_cutters.cutters import (
    FloatCutter,
    GroupCutter,
    ImmutableSequenceCutter,
    IntegerCutter,
    MutableSequenceCutter,
    OptionalCutter,
    ParagraphCutter,
    StringCutter,
    UnionCutter,
    UniqueMutableSequenceCutter,
    UniqueImmutableSequenceCutter,
    LiteralCutter,
    WordCutter,
)
from vkquick.ext.chatbot.exceptions import BadArgumentError
from vkquick.ext.chatbot.filters import (
    CommandFilter,
    IgnoreBotsMessagesFilter,
)
from vkquick.ext.chatbot.middlewares import MakeMessageProviderOnNewMessage
from vkquick.ext.chatbot.providers.attachment import (
    DocumentProvider,
    PhotoProvider,
)
from vkquick.ext.chatbot.providers.base import Provider
from vkquick.ext.chatbot.providers.message import (
    AnyMessageProvider,
    MessageProvider,
    TruncatedMessageProvider,
)
from vkquick.ext.chatbot.providers.page_entity import (
    GroupProvider,
    PageEntityProvider,
    UserProvider,
)
from vkquick.ext.chatbot.ui_builders.base import UIBuilder
from vkquick.ext.chatbot.ui_builders.button import Button, InitializedButton
from vkquick.ext.chatbot.ui_builders.carousel import Carousel, Element
from vkquick.ext.chatbot.ui_builders.keyboard import Keyboard
from vkquick.ext.chatbot.utils import (
    download_file,
    get_user_registration_date,
    random_id,
)
from vkquick.ext.chatbot.wrappers.attachment import (
    Attachment,
    Document,
    Photo,
)
from vkquick.ext.chatbot.wrappers.base import Wrapper
from vkquick.ext.chatbot.wrappers.message import Message, TruncatedMessage
from vkquick.ext.chatbot.wrappers.page_entities import Group, PageEntity, User

# Main core
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
from .bases.middleware import Middleware
from .bases.session_container import SessionContainerMixin
from .bot import Bot, EventProcessingContext
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
