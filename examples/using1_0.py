import os

import vkquick as vq


vq.current.objects["api"] = vq.API(os.getenv("VKDEVGROUPTOKEN"))
vq.current.objects["lp"] = vq.LongPoll(group_id=int(os.getenv("VKDEVGROUPID")))
bot = vq.Bot(event_handlers=[], signal_handlers=[])


@bot.event_handlers.append
@vq.Command(
    names=["foo", "bar"],
    prefixes=["/", "!"],
)
async def foo(user: vq.UserMention(), other: vq.Union(vq.Integer(), vq.Word())):
    """
    Какое-то описание команды. Lorem ipsum
    """
    return f"Hello! Num is {locals()}"


@bot.event_handlers.append
@vq.Command(
    names=["help"],
    prefixes=["/"],
)
async def help_(com_name: vq.String(), event: vq.CapturedEvent()):
    for event_handler in bot.event_handlers:
        if isinstance(event_handler, vq.Command) and com_name in event_handler.origin_names:
            return await vq.sync_async_run(event_handler.help_reaction(event))
    return f"Команды с именем `{com_name}` не существует!"


bot.run()
