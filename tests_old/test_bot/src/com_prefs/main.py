import vkquick as vq

from . import config
from tests.test_bot.src._add_cache import cache

TIMES = 1/16


@vq.Cmd(prefs=config.PREFS, names=config.NAMES)
@vq.Reaction("message_new")
def com_prefs():
    """
    Check working name and prefs in mix
    """
    global TIMES
    TIMES *= 2
    if TIMES == 1.0:
        cache("com_prefs")
    return config.ANSWER
