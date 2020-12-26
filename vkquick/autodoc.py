import typing as ty

from vkquick.bot import Bot
from vkquick.command import Command


def build_doc(bot: Bot, dir_path: str = "docs") -> None:
    ...


def init_files_content(commands: Command) -> ty.List[str]:
    ...
