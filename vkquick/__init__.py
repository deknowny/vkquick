"""
VK Quick — это высокоуровневная надстройка над API для ботов Вконтакте.
Инструменты, предлагаемые этим фреймворком, помогут Вам написать
мощного по возможностям и функционалу бота.
Большинство работы VK Quick берет на себя:
помощь разработчику в обработке содержимого команд,
огромное множество специальных оберток и функций,
создание документации к боту в виде команд в боте или же полноценного сайта
"""
from .current import fetch, curs
from .api import API, TokenOwner
from .bot import Bot
from .exceptions import VkApiError
from .signal import SignalCaller, SignalName, SignalHandler, ReservedSignal
from .debuggers import (
    ColoredDebugger,
    UncoloredDebugger,
    uncolored_text,
    Color,
)
from .utils import (
    AttrDict,
    SafeDict,
    peer,
    random_id,
    clear_console,
    sync_async_run,
)

from .json_parsers import BuiltinJSONParser

from .events_generators.event import Event
from .events_generators.longpoll import GroupLongPoll, UserLongPoll

from .event_handling.message import Message
from .event_handling.command import Command
from .event_handling.event_handler import EventHandler

from vkquick.text_arguments.mention import UserMention

from .event_handling.payload_arguments.sender import Sender
from .event_handling.payload_arguments.replied_user import RepliedUser
from .event_handling.payload_arguments.current import Current
from .event_handling.payload_arguments.captured_event import CapturedEvent
from .event_handling.payload_arguments.answer import Answer

from .event_handling.filters.enable import Enable, EnableStatus
from .event_handling.filters.direct_only import DirectOnly, DirectOnlyStatus
from .event_handling.filters.chat_only import ChatOnly, ChatOnlyStatus
from .event_handling.filters.ignore_bots_messages import (
    IgnoreBotsMessages,
    IgnoreBotsMessagesStatus,
)
from .event_handling.filters.retract_access_for import (
    RetractAccessFor,
    RetractAccessForStatus,
)
from .event_handling.filters.allow_access_for import (
    AllowAccessFor,
    AllowAccessForStatus,
)
from .event_handling.filters.action import Action, ActionStatus

from .base.payload_argument import PayloadArgument
from .base.text_values import TextBase
from .base.text_cutter import TextCutter
from .base.text_cutter import UnmatchedArgument
from .base.debugger import Debugger, HandlingStatus
from .base.wrapper import Wrapper
from .base.synchronizable import Synchronizable
from .base.json_parser import JSONParser
from .base.client import AsyncHTTPClient, SyncHTTPClient
from .base.user_type import UserType

from .wrappers.user import User, UserField, UserNameEnumCase

__version__ = "1.0.0a2"
