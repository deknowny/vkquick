import vkquick as vq

from . import config


@vq.Action("chat_invite_user", "chat_kick_user")
@vq.Reaction("message_new")
def greet(act: vq.Action):
    return act
