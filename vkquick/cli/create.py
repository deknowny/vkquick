import time
import os
import datetime
import pathlib
import typing as ty

import typer
import vkquick as vq


LICENSE_TEXT = """
Copyright (c) {year} {owner}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""".lstrip()

README = """
# {name}
![VK API library](https://bit.ly/3gdTRLC)

VK Bot. In developing now.
""".lstrip()

MAINPY = """
import vkquick as vq

import src.commands


bot = vq.Bot.init_via_token(
    "{token}"
)

for command in src.commands.__commands__:
    bot.add_command(command)


run = bot.run


if __name__ == "__main__":
    run()

""".lstrip()

HELPPY = """
import vkquick as vq


@vq.Command(
    prefixes=["/"],
    names=["help", "помощь"]
)
async def help_(ctx: vq.Context, com_name: str = vq.String()):
    \"""
    Показывает информацию по команде:
    способы использования, описание и примеры.
    \"""
    for command in ctx.shared_box.bot.commands:
        if com_name in command.names:
            return build_text(command)
    return f"Команды с именем `{com_name}` не существует!"


def build_text(com):
    prefixes = "\\n".join(
        map(lambda x: f"-> [id0|{x}&#8203;]", com.prefixes)
    )
    names = "\\n".join(map(lambda x: f"-> [id0|{x}&#8203;]", com.names))
    params_description = "\\n".join(
        f"[id0|{pos + 1}.] {arg[1].usage_description()}"
        for pos, arg in enumerate(com.reaction_arguments)
    )
    text = (
        f"{com.title}\\n\\n"
        f"{com.description}\\n\\n"
        "[Использование]\\n"
        f"Возможные префиксы:\\n{prefixes or '> Отсутствуют'}\\n"
        f"Возможные имена:\\n{names or '> Отсутствуют'}\\n"
        f"Аргументы, которые необходимо передать при вызове:\\n{params_description or 'Отсутствуют'}"
    )

    return text
""".lstrip()

READMEPY = """
import datetime
import platform

import vkquick as vq


creation_date = datetime.datetime.fromtimestamp({creation_timestamp})
now = datetime.datetime.now()
text = f\"""
Бот {bot_name}

<Описание>

Создан: {creation_date:%d.%m.%Y}
Создатель: {owner_mention}
Python: {platform.python_version()}

⚡️ Powered by [public195194058|VK Quick] ({vq.__version__}) 
\""".lstrip()


@vq.Command(
    prefixes=["::"],
    names=["readme"]
)
async def readme(ctx: vq.Context):
    \"""
    Сводка по боту.
    \"""
    await ctx.reply(text, disable_mentions=True)
""".lstrip()


COMMANDS_INIT = """
from .help_ import help_
from .readme import readme


__commands__ = [
    help_,
    readme,
]
""".lstrip()


def _validate_token(token: str) -> vq.API:

    if token.startswith("$"):
        # str.removeprefix...
        token = os.getenv(token[1:])
    return vq.API(token)


def fetch_group_and_user(
    api: vq.API,
) -> ty.Tuple[ty.Optional[vq.AttrDict], vq.User]:
    with api.synchronize():
        if api.token_owner == vq.TokenOwner.USER:
            creator = api.token_owner_user
            return None, creator
        else:
            groups = api.groups.get_by_id()
            group = groups[0]

            group_members = api.groups.get_members(
                filter="managers", group_id=group.id
            )
            for member in group_members.items:
                if member.role == "creator":
                    creator = api.fetch_user_via_id(member.id)
                    return group, creator

            raise ValueError("Can't get group's creator")


def _make_files(owner: vq.User, init: bool, bot_name: str, token: str):
    root_path = pathlib.Path()

    # Main bot's directory
    if init:
        bot_dir = root_path
    else:
        bot_dir = root_path / bot_name
        bot_dir.mkdir()

    license_ = bot_dir / "LICENSE"
    license_.touch()
    license_.write_text(
        LICENSE_TEXT.format(
            year=datetime.datetime.now().year,
            owner=format(owner, "{fn} {ln}"),
        ),
        encoding="utf-8",
    )

    readme = bot_dir / "README.md"
    readme.touch()
    readme.write_text(README.format(name=bot_name), encoding="utf-8")

    src = bot_dir / "src"
    src.mkdir()

    mainpy = src / "__main__.py"
    mainpy.touch()
    mainpy.write_text(
        MAINPY.format(token=token), encoding="utf-8",
    )

    commands = src / "commands"
    commands.mkdir()

    help_ = commands / "help_.py"
    help_.touch()
    help_.write_text(HELPPY, encoding="utf-8")

    readme = commands / "readme.py"
    readme.touch()
    readme.write_text(
        READMEPY.replace("{bot_name}", bot_name)
        .replace("{owner_mention}", owner.mention("{fn} {ln}"))
        .replace("{creation_timestamp}", str(int(time.time()))),
        encoding="utf-8",
    )

    commands_init = commands / "__init__.py"
    commands_init.touch()
    commands_init.write_text(COMMANDS_INIT, encoding="utf-8")


def create(
    bot_name: str,
    init: bool = False,
    api: str = typer.Option(
        ...,
        "-t",
        "--token",
        prompt="Enter an API token",
        callback=_validate_token,
    ),
):
    while True:
        group, creator = fetch_group_and_user(api)  # noqa

        if group is not None:
            confirmed = typer.confirm(
                f"\nYou want to create a bot "
                f"for a group\n<info>{group.name}</info> "
                f"<fg=white;options=blink>(https://vk.com/{group.screen_name})</>"
                f"\nContinue?",
                default=True,
            )
        else:
            owner_mention = format(creator, "{fn} {ln}")
            confirmed = typer.confirm(
                f"\nYou want to create a user bot "
                f"for the account\n<info>{owner_mention}</info>"
                f"\nContinue?",
                default=True,
            )
        if confirmed:
            _make_files(
                owner=creator, init=init, bot_name=bot_name, token=api.token
            )
            break
