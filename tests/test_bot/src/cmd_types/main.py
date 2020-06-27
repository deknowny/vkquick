import vkquick as vq

from . import config
from tests.test_bot.src._add_cache import cache


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def cmd_types(
    num: int, num_vq: vq.Integer(),
    word: vq.Word(),
    lit: vq.Literal("foo", "bar"),
    mention: vq.UserMention(),
    mentions: [vq.UserMention()],
    string: str,
    sender: vq.Sender()
):
    """
    Check types working
    """
    assert num == 123
    assert num_vq == 456
    assert lit == "foo"
    assert isinstance(mention, vq.User)
    assert isinstance(mentions, list)
    assert string == "long string"

    assert isinstance(sender, vq.User)


    cache("cmd_types")
    return config.ANSWER
