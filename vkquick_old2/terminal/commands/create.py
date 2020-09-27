import datetime
import pathlib

import cleo

from . import _files_content as fc


class Create(cleo.Command):
    """
    Create new bot

    create
        {name : Имя бота}
        {--o|owner=anonymous : Владелец бота. Добавляется в лицензионный файл}
        {--i|init : Инициализация бота внутри текущей директории}
    """

    def handle(self):
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
            fc.LICENSE.format(
                year=datetime.datetime.now().year, owner=self.option("owner")
            )
        )

        readme = bot_dir / "README.md"
        readme.touch()
        readme.write_text(fc.README.format(name=self.argument("name")))

        config = bot_dir / "config.py"
        config.touch()
        config.write_text(fc.CONFIG)

        # Code
        src = bot_dir / "src"
        src.mkdir()

        main = src / "__main__.py"
        main.touch()
        main.write_text(fc.MAIN)

        init = src / "__init__.py"
        init.touch()

        # Docs
        docs = bot_dir / "docs"
        docs.mkdir()

        # Logs
        logs = bot_dir / "logs"
        logs.mkdir()
