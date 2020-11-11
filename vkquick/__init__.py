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
from .exceptions import VkApiError
from .events_generators.event import Event
from .debuggers import (
    ColoredDebugger,
    UncoloredDebugger,
    uncolored_text,
    Color,
)
from .signal import (
    SignalCaller,
    SignalName,
    SignalHandler,
    ReservedSignal,
    signal_handler,
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
from .clients import AIOHTTPClient, RequestsHTTPClient

from .events_generators.event import Event
from .events_generators.longpoll import GroupLongPoll, UserLongPoll

from .context import Context
from .command import Command

from .text_cutters.integer import Integer
from .text_cutters.word import Word
from .text_cutters.bool_ import Bool
from .text_cutters.list_ import List
from .text_cutters.mention import UserMention
from .text_cutters.union import Union
from .text_cutters.string_ import String
from .text_cutters.optional import Optional
from .text_cutters.regex import Regex

from .base.text_values import TextBase
from .base.text_cutter import TextCutter
from .base.text_cutter import UnmatchedArgument
from .base.debugger import Debugger
from .base.handling_status import HandlingStatus
from .base.wrapper import Wrapper
from .base.synchronizable import Synchronizable
from .base.json_parser import JSONParser
from .base.client import AsyncHTTPClient, SyncHTTPClient

from .filters.action import Action
from .filters.allow_access_for import AllowAccessFor
from .filters.chat_only import ChatOnly
from .filters.direct_only import DirectOnly
from .filters.ignore_bots_messages import IgnoreBotsMessages
from .filters.retract_access_for import RetractAccessFor

from .wrappers.user import User, UserField, UserNameEnumCase
from vkquick.wrappers.message import Message, ClientInfo

from .bot import Bot


__version__ = "1.0.0b0"
