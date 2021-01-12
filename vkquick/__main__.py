"""
Запуск CLI

Всю информацию можно найти по

    python -m vkquick --help

Либо по конкретной команде

    python -m vkquick new --help

Если с установкой все было в порядке, скрипт занесется в `PATH`
и вместо `python -m vkquick` можно писать `vq`
"""
import typer

from vkquick.cli.create import create
from vkquick.cli.make import make_typer
from vkquick.cli.run import run_typer

app = typer.Typer(name="VK Quick CLI")
app.add_typer(make_typer, name="make")
app.add_typer(run_typer, name="run")
app.command()(create)


if __name__ == "__main__":
    app()
