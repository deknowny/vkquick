"""
Help you create the best VK chat-bots ever.

More info [here](https://vkquick.github.io)
"""

from . import current
from .api import API
from .bot import Bot
from .exception import VkErr
from .lp import LongPoll
from .signal import Signal, SignalsList, signal
from .reaction import Reaction, ReactionsList


from .annotypes import *
from .validators import *
from .tools import *


__version__ = "0.2.6"
