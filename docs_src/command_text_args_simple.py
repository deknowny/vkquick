import vkquick as vq

bot = vq.Bot.init_via_token("token")


@bot.command(
    prefixes="/"
    names="foo"
)
def foo(num: vq.Integer):
    return f"Команда вызвана с числом {num}"


bot.run()
