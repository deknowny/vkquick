import vkquick as vq
import pytest

from . import config
from tests.test_bot.src._add_cache import cache


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
async def apireq(event: vq.Event(), api: vq.API):
    """
    Handler to command `apireq`
    """
    await api.users.get()

    await api.messages.getConversationMembers(
        peer_id=event.object.message.peer_id
    )

    await api.messages.get_conversation_members(
        peer_id=event.object.message.peer_id
    )

    with pytest.raises(vq.VkErr):
        await api.asdasdasd.asdasd_asdasdSDFsdfgdfgsdfsadfsadfsdfsdfasd()

    cache("apireq")

    return config.ANSWER
