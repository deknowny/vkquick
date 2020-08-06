"""
Набор полезных инструмеентов,
встречающихся повсеместно как в ботах (клавиатуры, Message-объекты...),
так и внутри vkquick
"""
from random import randint

from .message import Message
from .user import User, UserAnno

# UI
from .button import Button
from .keyboard import Keyboard
from .template import Template
from .element import Element

# Uploaders
from .photo import Photo
from .uploader import Uploader
from .doc import Doc


PEER: int = int(2e9)
"""
Число, разделающее peer_id на
диалоги с пользователями и беседы.

== 2_000_000_000
"""


def random_id(side: int = 2 ** 31) -> int:
    """
    Случайное число в дипазоне +-`side`.
    Используется для метода ```messages.send``` или в классе `vkquick.tools.message.Message`
    """
    return randint(-side, +side)
