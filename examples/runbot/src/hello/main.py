import vkquick as vq

from . import config


@vq.Cmd(
    prefs=config.PREFS,
    names=config.NAMES
)
@vq.Reaction("message_new")
async def hello(sender: vq.Sender, event: vq.Event):
    return f"{sender:<fn>}\n{event}"
