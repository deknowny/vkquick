import vkquick as vq

from . import config
from tests.test_bot.src._add_cache import cache


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
async def call_signal(bot: vq.Bot):
    """
    Handler to command `call_signal`
    """
    await bot.signals.resolve("custom_signal", some_arg=True)
    return config.ANSWER
