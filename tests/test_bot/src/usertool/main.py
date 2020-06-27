import vkquick as vq

from . import config
from tests.test_bot.src._add_cache import cache


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
async def usertool(api: vq.API):
    """
    Handler to command `usertool`
    """
    cache("usertool")
    user = await api.users.get(
        user_ids="1"
    )
    user = user[0]
    vq_user = await vq.User(user_id=1).get_info()
    assert user == vq_user.info
    assert f"[id{user['id']}|{user['first_name']} {user['last_name']}]" == (
        vq_user.mention("<fn> <ln>")
    )
    assert f"{user['first_name']} {user['last_name']}" == (
        f"{vq_user:<info.first_name> <info.last_name>}"
    )
    return config.ANSWER
