import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def foo(sender: vq.Sender()):
    """
    Handler to command `foo`
    """
    return config.ANSWER
