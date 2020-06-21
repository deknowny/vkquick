import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def fizz():
    """
    Handler to command `fizz`
    """
    return config.ANSWER