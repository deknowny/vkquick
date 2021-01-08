import re

import vkquick as vq


bot = vq.Bot.init_via_token("token")


@bot.add_command(names=r"foo\s*bar", routing_command_re_flags=re.IGNORECASE | re.DOTALL)
def foo():
    return "Hello!"


bot.run()
