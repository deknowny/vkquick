import os

import vkquick as vq


@vq.Command(
    names=["foo"],
    prefixes=["/"],
    on_unapproved_filters={vq.Enable: lambda _: "Disabled"},
)
async def foo(user: vq.UserMention()):
    return f"Hello! Num is {locals()}"


vq.current.objects["api"] = vq.API(os.getenv("VKDEVGROUPTOKEN"))
vq.current.objects["lp"] = vq.LongPoll(group_id=int(os.getenv("VKDEVGROUPID")))
bot = vq.Bot(event_handlers=[foo], signal_handlers=[])


@bot.event_handlers.append
@vq.Command(
    names=["help"],
    prefixes=["/"],
)
async def help_(com_name: vq.String(), event: vq.CapturedEvent()):
    for event_handler in bot.event_handlers:
        if isinstance(event_handler, vq.Command) and com_name in event_handler.origin_names:
            return await vq.sync_async_run(event_handler.help_reaction(event))


bot.run()
