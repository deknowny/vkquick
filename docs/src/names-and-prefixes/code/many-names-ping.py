import vkquick as vq


app = vq.App()


@app.command("ping", "пинг")
async def multi_name_ping():
    return "Pong!"


app.run("$BOT_TOKEN")