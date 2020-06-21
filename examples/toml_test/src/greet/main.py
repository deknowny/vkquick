import vkquick as vq

from . import config


@vq.Action("chat_kick_user")
@vq.Reaction("message_new")
def greet():
    """
    Handler to command `greet`
    """
    return config.ANSWER
