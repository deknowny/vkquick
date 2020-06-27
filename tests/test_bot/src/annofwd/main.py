import vkquick as vq

from . import config
from tests.test_bot.src._add_cache import cache


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
async def annofwd(fwds: vq.FwdUsers("verificate")):
    """
    Get fwd users
    """
    user = await vq.User(user_id=fwds[0].id).get_info("verificate")
    assert user.info == fwds[0].info
    cache("annofwd")
    return config.ANSWER
