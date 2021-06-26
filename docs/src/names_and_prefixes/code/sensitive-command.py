import vkquick as vq


app = vq.App()


@app.command("ping", routing_re_flags=0)
async def pong():
    return "Pong!"


app.run("$BOT_TOKEN")