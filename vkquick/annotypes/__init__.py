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

from .event import Event
from .sender import Sender
from .replied_user import RepliedUser
from .fwd_users import FwdUsers
