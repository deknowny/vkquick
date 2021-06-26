import vkquick as vq


app = vq.App()


@app.command("ping", prefixes=["/"])
async def pong():
    return "Pong!"


app.run("$BOT_TOKEN")