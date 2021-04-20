import vkquick as vq

bot = vq.Bot.init_via_token("token")


@bot.command(prefixes="/", names="hi")
def hi():
    return "Hello!"


bot.run()
