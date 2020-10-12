import os

import vkquick as vq


@vq.Enable(False)
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

bot.run()
