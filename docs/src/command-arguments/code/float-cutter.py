import vkquick as vq


app = vq.App()


@app.command("add")
async def add(num1: float, num2: float):
    return f"Сумма двух чисел: {num1 + num2}"


app.run("$BOT_TOKEN")