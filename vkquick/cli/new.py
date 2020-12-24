import datetime
import pathlib
import os
import time
import typing as ty

import cleo

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

import src.default.help_
import src.default.readme


bot = vq.Bot.init_via_token(
    "{token}"
)

bot.mark.command(src.default.help_.help_)
bot.mark.command(src.default.readme.readme)


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


class New(cleo.Command):
    """
    Создает заготовку файлов для бота

    new
        {name : Имя бота}
        {--o|owner : Владелец бота. Добавляется в лицензионный файл. По умолчанию назначается создатель сообщества/владелец токена пользователя}
        {--i|init : Инициализация бота внутри текущей директории}
        {--t|token= : API токен}
    """

    def handle(self):

        while True:
            current_group, owner = self._get_info_by_token()

            if current_group is not None:
                confirmed = self.confirm(
                    f"\nYou want to create a bot "
                    f"for a group\n<info>{current_group.name}</info> "
                    f"<fg=white;options=blink>(https://vk.com/{current_group.screen_name})</>"
                    f"\nContinue?",
                    True,
                )
            else:
                owner_mention = format(owner, "{fn} {ln}")
                confirmed = self.confirm(
                    f"\nYou want to create a user bot "
                    f"for the account\n<info>{owner_mention}</info>"
                    f"\nContinue?",
                    True,
                )
            if confirmed:
                self._make_files(owner)
                break

    def _fetch_group_and_user(self) -> ty.Tuple[vq.AttrDict, vq.User]:
        with self.api.synchronize():
            group = self.api.groups.get_by_id()
            group = group[0]

            group_members = self.api.groups.getMembers(
                filter="managers", group_id=group.id
            )
            for member in group_members.items:
                if member.role == "creator":
                    creator_id = member.id
                    creator = self.api.users.get(user_ids=creator_id)
                    creator = vq.User(creator[0])
                    return group, creator

            raise ValueError("Can't get group's creator")

    def _fetch_user(self):
        with self.api.synchronize():
            user = self.api.users.get()
            user = vq.User(user[0])
            return None, user

    def _get_info_by_token(
        self,
    ) -> ty.Tuple[ty.Optional[vq.AttrDict], vq.User]:
        if not self.option("token"):
            self.token = self.ask("Enter an API token:")
        else:
            self.token = self.option("token")

        if self.token.startswith("$"):
            # str.removeprefix... Когда-нибудь...
            self.token = os.getenv(self.token[1:])

        self.api = vq.API(self.token)

        if self.api.token_owner == vq.TokenOwner.GROUP:
            return self._fetch_group_and_user()
        else:
            return self._fetch_user()

    def _make_files(self, owner: vq.User):
        root_path = pathlib.Path()

        # Main bot's directory
        if self.option("init"):
            bot_dir = root_path
        else:
            bot_dir = root_path / self.argument("name")
            bot_dir.mkdir()

        license_ = bot_dir / "LICENSE"
        license_.touch()
        license_.write_text(
            LICENSE_TEXT.format(
                year=datetime.datetime.now().year,
                owner=self.option("owner") or format(owner, "{fn} {ln}"),
            ),
            encoding="utf-8",
        )

        readme = bot_dir / "README.md"
        readme.touch()
        readme.write_text(
            README.format(name=self.argument("name")), encoding="utf-8"
        )

        src = bot_dir / "src"
        src.mkdir()

        mainpy = src / "__main__.py"
        mainpy.touch()
        mainpy.write_text(
            MAINPY.format(token=self.token), encoding="utf-8",
        )

        default = src / "default"
        default.mkdir()

        help_ = default / "help_.py"
        help_.touch()
        help_.write_text(HELPPY, encoding="utf-8")

        readme = default / "readme.py"
        readme.touch()
        readme.write_text(
            READMEPY.replace("{bot_name}", self.argument("name"))
            .replace("{owner_mention}", owner.mention("{fn} {ln}"))
            .replace("{creation_timestamp}", str(int(time.time()))),
            encoding="utf-8",
        )
