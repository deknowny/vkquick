import os

import vkquick as vq


@vq.Command(
    names=["foo"],
    prefixes=["/"],
)
async def foo(num: vq.Bool()):
    return f"Hello! Num is {locals()}"


vq.current.objects["api"] = vq.API(os.getenv("VKDEVGROUPTOKEN"))
vq.current.objects["lp"] = vq.LongPoll(group_id=int(os.getenv("VKDEVGROUPID")))
bot = vq.Bot(event_handlers=[foo], signal_handlers=[])

bot.run()
