import vkquick as vq

from . import config


@vq.Cmd(
    prefs=config.PREFS,
    names=config.NAMES
)
@vq.Reaction("message_new")
def hello():
    return config.ANSWER
