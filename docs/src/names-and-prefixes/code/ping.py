import vkquick as vq


app = vq.App()


@app.command("ping")
async def pong():
    return "Pong!"


app.run("$BOT_TOKEN")