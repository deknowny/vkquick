import vkquick as vq

from . import config
from tests.test_bot.src._add_cache import cache


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def cmd_insensetive():
    """
    Test insensetive
    """
    cache("cmd_insensetive")
    return config.ANSWER
