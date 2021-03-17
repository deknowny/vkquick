import vkquick as vq

bot = vq.Bot.init_via_token("token")


@bot.add_command(names=["hi", "привет"])
def hi():
    return "Hello!"


bot.run()
