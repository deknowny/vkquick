import os

import vkquick as vq


# Самая обычная команда, которая отвечает `hello!`
@vq.Command(names=["hi"])
def hi():
    return "hello!"


bot = vq.Bot.init_via_token(os.getenv("VKDEVGROUPTOKEN"))
bot.event_handlers.append(hi)
bot.run()