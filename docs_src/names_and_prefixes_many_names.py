import vkquick as vq

bot = vq.Bot.init_via_token("token")


@bot.command(names=["hi", "привет"])
def hi():
    return "Hello!"


bot.run()
