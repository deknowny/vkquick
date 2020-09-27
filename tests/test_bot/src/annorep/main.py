import vkquick as vq

from . import config
from tests.test_bot.src._add_cache import cache


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
async def annorep(rep: vq.RepliedUser("verificate")):
    """
    Get rep user
    """
    user = await vq.User(user_id=rep.id).get_info("verificate")
    assert user.info == rep._info
    cache("annorep")
    return config.ANSWER
