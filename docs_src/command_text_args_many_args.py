import vkquick as vq

bot = vq.Bot.init_via_token("token")


@bot.add_command(
    prefixes="/"
    names="add"
)
def foo(name: vq.Word, age: vq.Integer):
    # Какие-то манипуляции...
    return f"Пользователь с именем `{name}` и возрастом `{age}` добавлен!"


bot.run()
