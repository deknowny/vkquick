import vkquick as vq

bot = vq.Bot.init_via_token("token")


@bot.command(names=r"foo\d", use_regex_escape=False)
def foo():
    return "Hello!"


bot.run()
