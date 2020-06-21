import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def bar(text: vq.Word(), event: vq.Event):
    """
    Handler to command `bar`
    """
    return config.ANSWER
