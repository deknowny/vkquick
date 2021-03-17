import vkquick as vq

bot = vq.Bot.init_via_token("token")


@bot.add_command(prefixes="/", names="hi")
def hi():
    return "Hello!"


bot.run()
