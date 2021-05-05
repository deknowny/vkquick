import importlib.metadata

# Main core
from .base.api_serializable import APISerializableMixin
from .base.event import BaseEvent
from .base.event_factories import BaseEventFactory, BaseLongPoll
from .base.json_parser import BaseJSONParser


from .cached_property import cached_property
from .event import GroupEvent, UserEvent
from .json_parsers import (
    BuiltinJsonParser,
    OrjsonParser,
    UjsonParser,
    json_parser_policy,
)
from .longpoll import GroupLongPoll, UserLongPoll
from .pretty_view import pretty_view
from .exceptions import VKAPIError
from .api import API, TokenOwner


# from vkquick.ext.chatbot.providers.attachment import (
#     DocumentProvider,
#     PhotoProvider,
# )
# from vkquick.ext.chatbot.base.provider import Provider
# from vkquick.ext.chatbot.providers.message import (
#     AnyMessageProvider,
#     MessageProvider,
#     TruncatedMessageProvider,
# )
# from vkquick.ext.chatbot.providers.page import (
#     GroupProvider,
#     PageProvider,
#     UserProvider,
# )
# from vkquick.ext.chatbot.ui_builders.base import UIBuilder
# from vkquick.ext.chatbot.ui_builders.button import Button, InitializedButton
# from vkquick.ext.chatbot.ui_builders.carousel import Carousel, Element
# from vkquick.ext.chatbot.ui_builders.keyboard import Keyboard
# from vkquick.ext.chatbot.wrappers.attachment import (
#     Attachment,
#     Document,
#     Photo,
# )
# from vkquick.ext.chatbot.base.wrapper import Wrapper
# from vkquick.ext.chatbot.wrappers.message import Message, TruncatedMessage
# from vkquick.ext.chatbot.wrappers.page import Group, Page, User


__version__ = importlib.metadata.version(__name__)
