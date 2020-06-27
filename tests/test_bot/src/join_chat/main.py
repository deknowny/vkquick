import vkquick as vq

from . import config
from tests.test_bot.src._add_cache import cache


@vq.Action("chat_invite_user")
@vq.Reaction("message_new")
def join_chat():
    """
    Handler to command `leave_chat`
    """
    cache("join_chat")
    return config.ANSWER
