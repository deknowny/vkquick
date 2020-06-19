from .message import Message
from .payload import Payload
from .user import User, UserAnno

# UI
from .button import Button
from .keyboard import Keyboard
from .template import Template
from .element import Element


PEER = int(2e9)


def random_id(side: int = 2**31):
    """
    Random int between +-`side` parametr.
    Use for messages.send or Message class
    """
    return randint(-side, +side)
