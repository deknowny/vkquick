import vkquick as vq


app = vq.App(prefixes=["/", "!"])


@app.command("ping")
async def pong():
    return "Pong!"


@app.command("echo")
async def pong():
    return "Hi!"


app.run("$BOT_TOKEN")