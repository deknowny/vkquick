import vkquick as vq
import attrdict

from . import config
from tests.test_bot.src._add_cache import cache


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
async def annotypes1(
    sender: vq.Sender("verificate"),
    event_brackets: vq.Event(), event: vq.Event,
    api: vq.API,
    client_info_brackets: vq.ClientInfo(), client_info: vq.ClientInfo

):
    """
    Annotypes
    """

    assert client_info_brackets == client_info and isinstance(
        client_info, attrdict.AttrMap
    )
    assert api is vq.current.api
    assert event_brackets == event and isinstance(
        event, attrdict.AttrMap
    )

    user = await vq.User(user_id=sender.id).get_info("verificate")
    assert user.info == sender._info
    cache("annotypes1")

    return config.ANSWER
