import os

import vkquick as vq


@vq.Command(
    names=["foo"],
    prefixes=["/"],
    on_invalid_text_argument={
        "num2": lambda **_: "Fizz"
    }
)
async def foo(num: vq.Integer, num2: vq.Integer):
    return f"Hello! Num is {num} and {num2}"


vq.current.objects["api"] = vq.API(os.getenv("VKDEVGROUPTOKEN"))
vq.current.objects["lp"] = vq.LongPoll(group_id=int(os.getenv("VKDEVGROUPID")))
bot = vq.Bot(event_handlers=[foo], signal_handlers=[])

bot.run()
