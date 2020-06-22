import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES, argline=r"\+a{name}")
@vq.Reaction("message_new")
def foo(name: vq.Word(), sender: vq.Sender()):
    """
    Handler to command `foo`
    """
    return vq.Message(name)
