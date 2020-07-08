"""
.. include:: ./guide.md
"""

from . import current
from .api import API
from .bot import Bot
from .exception import VkErr
from .lp import LongPoll
from .signal import Signal, SignalsList
from .reaction import Reaction, ReactionsList


from .annotypes import *
from .validators import *
from .tools import *


__version__ = "0.1.0rc1"
