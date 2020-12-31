# TODO: appears in 1.1
import typing as ty

from vkquick.bot import Bot
from vkquick.command import Command


_command_template = """
# {title}
> {simple_usage}
{description}

***

### Префиксы
{prefixes}

### Имена
{names}

### Аргументы
{arguments}
""".rstrip()


def build_doc(bot: Bot, dir_path: str = "docs") -> None:
    docs = init_files_content(bot.commands)


def init_files_content(commands: ty.List[Command]) -> ty.List[str]:
    docs = [_build_doc_for_command(command) for command in commands]
    return docs


def _build_doc_for_command(command: Command) -> str:
    ...
