"""
Аннотационные типы для реакций.
Класс также является аннотационным,
если наследуется `vkquick.annotypes.base.Annotype`
"""
from .base import Annotype

from .command_types import Word
from .command_types import Integer
from .command_types import List
from .command_types import String
from .command_types import UserMention
from .command_types import CommandArgument
from .command_types import Literal
from .command_types import Custom
from .command_types import Optional

from .event import Event
from .sender import Sender
from .replied_user import RepliedUser
from .fwd_users import FwdUsers
from .client_info import ClientInfo
from .peer_id import PeerID
from .group_id import GroupID
from .chat_id import ChatID
from .callback_answer import CallbackAnswer
