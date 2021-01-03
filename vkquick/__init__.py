"""
VK Quick — это высокоуровневная надстройка над API для ботов Вконтакте.
Инструменты, предлагаемые этим фреймворком, помогут Вам написать
мощного по возможностям и функционалу бота.
Большинство работы VK Quick берет на себя:
помощь разработчику в обработке содержимого команд,
огромное множество специальных оберток и функций,
создание документации к боту в виде команд в боте или же полноценного сайта
"""
from .api import API, TokenOwner
from .exceptions import VkApiError
from .events_generators.event import Event
from .debuggers import (
    ColoredDebugger,
    UncoloredDebugger,
    uncolored_text,
    Color,
)
from .signal import SignalHandler, EventHandler

from .utils import (
    AttrDict,
    SafeDict,
    peer,
    random_id,
    clear_console,
    sync_async_run,
    sync_async_callable,
    download_file,
    get_user_registration_date,
    pretty_view,
)

from .json_parsers import (
    JsonParser,
    UjsonParser,
    OrjsonParser,
    json_parser_policy,
)

from .events_generators.event import Event
from .events_generators.longpoll import GroupLongPoll, UserLongPoll

from .context import Context
from .command import Command

from .text_cutters.integer import Integer
from .text_cutters.word import Word
from .text_cutters.bool_ import Bool
from .text_cutters.list_ import List
from .text_cutters.mention import UserMention, GroupMention
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
from .base.synchronizable import Synchronizable, synchronizable_function
from .base.json_parser import JSONParser
from .base.serializable import APISerializable
from .base.filter import Filter

from .filters.action import Action
from .filters.enable import Enable
from .filters.allow_access_for import AllowAccessFor
from .filters.chat_only import ChatOnly
from .filters.direct_only import DirectOnly
from .filters.ignore_bots_messages import IgnoreBotsMessages
from .filters.retract_access_for import RetractAccessFor
from .filters.required_attachments import RequiredAttachments

from .wrappers.user import User
from .wrappers.attachment import Document, Photo
from .wrappers.message import Message

from .uploaders import (
    upload_photo_to_message,
    upload_photos_to_message,
    upload_doc_to_message,
)

from .bot import Bot, async_run_many_bots, run_many_bots

from .keyboard import Keyboard
from .button import Button
from .carousel import Carousel, Element

from .shared_box import SharedBox


__version__ = "1.0.0b6"
