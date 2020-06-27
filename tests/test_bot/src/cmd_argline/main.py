import vkquick as vq

from . import config
from tests.test_bot.src._add_cache import cache


@vq.Cmd(names=config.NAMES, argline="_{arg}")
@vq.Reaction("message_new")
def cmd_argline(arg: int):
    """
    Check argline working
    """
    cache("cmd_argline")
    return config.ANSWER
