import pathlib
import re
import typing as ty

import typer

make_typer = typer.Typer()


COMMAND_TEMPLATE = """
import vkquick as vq


@vq.Command(
    {params}
)
def {name}({args}):{docstring}
    return f"Команда `{name}` работает!"
""".lstrip()


def _name_checker(name: str):
    match = re.fullmatch("[_a-zA-Z][_a-zA-Z0-9]+", name)
    if match is None:
        raise typer.BadParameter(
            "Name should match for regex `[_a-zA-Z][_a-zA-Z0-9]+`"
        )
    return name


@make_typer.command()
def com(
    command_name: str = typer.Argument(..., callback=_name_checker),
    names: ty.List[str] = typer.Option([], "-n", "--name"),
    prefixes: ty.List[str] = typer.Option([], "-p", "--prefix"),
    title: ty.Optional[str] = typer.Option(None, "-t", "--title"),
    description: ty.Optional[str] = typer.Option(None, "-d", "--description"),
    args: ty.List[str] = typer.Option([], "-a", "--arg"),
    show: bool = typer.Option(False, "-s", "--show"),
):
    if not names:
        names = [command_name]

    command_params = [f"names={names}".replace("'", '"')]

    if prefixes:
        command_params.append(f"prefixes={list(prefixes)}".replace("'", '"'))

    if title:
        command_params.append(f'title="{title}"')

    if description:
        docstring = f'\n    """\n    {description}\n    """'
    else:
        docstring = ""

    args = ", ".join(args)

    command_params = ",\n    ".join(command_params)

    command_code = COMMAND_TEMPLATE.format(
        params=command_params,
        name=command_name,
        args=args,
        docstring=docstring,
    )

    if show:
        print(command_code)
    else:
        commands = pathlib.Path("src") / "commands"
        if not commands.exists():
            raise FileNotFoundError(
                "This command should be run from root "
                "of the bot's project that was "
                "created via CLI"
            )
        command = commands / f"{command_name}.py"
        command.touch()
        command.write_text(command_code, encoding="utf-8")

        commands_init = commands / "__init__.py"
        commands_config = commands_init.read_text(encoding="utf-8")
        commands_config_new = commands_config.replace(
            "]", f"    {command_name},\n]"
        )
        commands_config_new = f"from .{command_name} import {command_name}\n{commands_config_new}"
        commands_init.write_text(commands_config_new, encoding="utf-8")
