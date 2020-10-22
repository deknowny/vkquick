"""
VK Quick — это высокоуровневная надстройка над API для ботов Вконтакте.
Инструменты, предлагаемые этим фреймворком, помогут Вам написать
мощного по возможностям и функционалу бота.
Большинство работы VK Quick берет на себя:
помощь разработчику в обработке содержимого команд,
огромное множество специальных оберток и функций,
создание документации к боту в виде команд в боте или же полноценного сайта
"""
from . import current
from .api import API, TokenOwner
from .bot import Bot
from .exceptions import VkApiError
from .utils import (
    peer,
    random_id,
    sync_async_run,
    AttrDict,
    JSONParserBase,
    BuiltinJSONParser,
    OrjsonJSONParser,
    RequestsSession,
    SafeDict,
)

from .events_generators.event import Event
from .events_generators.longpoll import GroupLongPoll, UserLongPoll

from .event_handling.message import Message
from .event_handling.command import Command
from .event_handling.event_handler import EventHandler
from .event_handling.handling_info_scheme import HandlingInfoScheme

from .event_handling.reaction_argument.text_arguments.base import TextArgument
from .event_handling.reaction_argument.text_arguments.base import (
    UnmatchedArgument,
)
from .event_handling.reaction_argument.text_arguments.integer import Integer
from .event_handling.reaction_argument.text_arguments.word import Word
from .event_handling.reaction_argument.text_arguments.string_ import String
from .event_handling.reaction_argument.text_arguments.union import Union
from .event_handling.reaction_argument.text_arguments.regex import Regex
from .event_handling.reaction_argument.text_arguments.bool_ import Bool
from .event_handling.reaction_argument.text_arguments.mention import (
    UserMention,
)
from .event_handling.reaction_argument.text_arguments.text_values_base import (
    TextBase,
)

from .event_handling.reaction_argument.payload_arguments.base import (
    PayloadArgument,
)
from .event_handling.reaction_argument.payload_arguments.sender import Sender
from .event_handling.reaction_argument.payload_arguments.replied_user import (
    RepliedUser,
)
from .event_handling.reaction_argument.payload_arguments.captured_event import (
    CapturedEvent,
)

from .event_handling.filters.base import Filter
from .event_handling.filters.enable import Enable

from .wrappers.base import Wrapper
from .wrappers.user import User


__version__ = "1.0.0a0"
