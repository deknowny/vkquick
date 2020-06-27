import asyncio

import vkquick as vq


def main_user():
    api = vq.API(
        token=vq.current.bot.config.tests.user_token,
        version=vq.current.bot.config.api.version,
        owner="user"
    )
    api._delay = 2
    msg.api = api
    asyncio.run(_commands(api))


async def msg(text, **kwargs):
    await msg.api.messages.send(
        peer_id=vq.current.bot.config.tests.peer_id,
        message=text,
        random_id=vq.random_id(),
        **kwargs
    )


async def _commands(api):
    await asyncio.sleep(2)

    await msg("send_photo")

    await msg("apireq")

    await msg("doc_uploader")

    await msg("cmd_inSensETive")

    await msg("cmd_argline_123")

    await msg("cmd_types 123 456 abc  foo @deknowny @deknowny @deknowny   long string")

    await msg("/com_prefs")
    await msg("!com_prefs")
    await msg("/com with prefix")
    await msg("!com with prefix")

    await msg("annotypes1")

    await msg("annofwd", forward_messages="3383342")

    await msg("annorep", reply_to="3383342")

    me = await api.users.get()
    me = me[0]

    await api.messages.remove_chat_user(
        chat_id=vq.current.bot.config.tests.peer_id - vq.PEER,
        user_id=me["id"]
    )

    await msg("return")

    await msg("usertool")

    await msg("call_signal")



    await asyncio.sleep(2)

    # Teardown the bot
    vq.current.bot.reaload_now = True
