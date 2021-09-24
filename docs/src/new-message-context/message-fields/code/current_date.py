import vkquick as vq


app = vq.App()


@app.command("date", prefixes=["/"])
async def current_date(ctx: vq.NewMessage):
    human_format_date = ctx.msg.date.isoformat(sep=" ")
    return f"Сейчас {human_format_date}"


app.run("$BOT_TOKEN")