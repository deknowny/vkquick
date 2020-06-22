import datetime
import os
import subprocess
import sys
import shutil
from pathlib import Path

import click
import toml
import attrdict
import vkquick as vq
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


MIT = """
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
""".strip()

# TODO: Add a link, where read more
CONFIG_TOML = """
[api]
token = "{token}"
group_id = {group_id}
delay = 0.05
version = 5.124


[longpoll]
wait = 25
""".strip()


README = """
# {name}
VK Bot written on vkquick. Now is in developing.
""".strip()


COMMAND = """
import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def {name}():
    \"""
    Handler to command `{name}`
    \"""
    return config.ANSWER
""".strip()


CONFIG = """
NAMES = ["{name}"]
ANSWER = "You used `{name}` command!"
""".strip()


SIGNAL = """
import vkquick as vq


@vq.Signal("{name}")
def {name}():
    \"""
    Handler to signal `{name}`
    \"""
""".strip()


@click.group()
def bot():
    ...


@click.option(
    "-o",
    "--owner",
    default="Anonymous",
    help="Bot owner. Will be added to a license file",
)
@click.option(
    "-t", "--token",
    default="",
    help="Token for group bot"
)
@click.option(
    "-gi", "--group-id", "group_id",
    default=0,
    type=int,
    help="Token's group ID"
)
@click.argument("name")
@bot.command()
def new(owner, name, token, group_id):
    """
    Create a new bot
    """
    year = datetime.datetime.now().year
    bot_path = Path(name)
    src_path = Path(name) / "src"
    os.makedirs(str(src_path))
    with open(bot_path / "LICENSE", "w+") as file:
        file.write(
            MIT.format(owner=owner, year=year)
        )
    with open(bot_path / "config.toml", "w+") as file:
        file.write(
            CONFIG_TOML.format(
                token=token, group_id=group_id
            )
        )
    with open(bot_path / "README.md", "w+") as file:
        file.write(
            README.format(name=name.title())
        )

    open(src_path / "__init__.py", "w+")

    click.echo(
        click.style("Created ", fg="green") +\
        click.style(name, fg="cyan", bold=True) +\
        click.style(" bot. ", fg="green") +\
        click.style("Don't forget `cd` to bot's directory", fg="green")
    )
    if not (token and group_id):
        click.echo(
            click.style("\nPlease, add following parameters to ", fg="yellow") +\
            click.style(str(Path(name) / "config.toml"), fg="cyan", bold=True) +\
            click.style(" under ", fg="yellow") +\
            click.style("[api]", fg="cyan", bold=True) +\
            click.style(" section", fg="yellow")
        )
        if not token:
            click.echo(
                " -- " +\
                click.style("token", fg="red", bold=True)
            )
        if not group_id:
            click.echo(
                " -- " +\
                click.style("group_id", fg="red", bold=True)
            )


@click.option(
    "-d", "--delete",
    is_flag=True,
    default=False,
    help="Delete the com"
)
@click.argument("name")
@bot.command()
def com(name, delete):
    """
    Create a new command in the bot
    """
    if delete:
        click.echo(
            click.style("Command ", fg="yellow") +\
            click.style(name, bold=True, fg="cyan") +\
            click.style(" will be removed. Continue? ", fg="yellow") +\
            click.style("(y/any)", bold=True),
            nl=False
        )
        confirm = click.getchar()
        click.echo()
        if confirm == "y":
            shutil.rmtree(Path("src") / name, ignore_errors=True)
            with open(Path("src") / "__init__.py", "r") as file:
                new_text = file.read().replace(f"from .{name} import {name}\n", "")
            with open(Path("src") / "__init__.py", "w") as file:
                file.write(new_text)

            click.echo(
                click.style("Command ", fg="green") +\
                click.style(name, bold=True, fg="cyan") +\
                click.style(" has been removed", fg="green")
            )

        else:
            click.secho("Files haven't been changed", fg="red")

    else:
        com_path = Path("src") / name
        os.makedirs(str(com_path))
        with open(com_path / "main.py", "w+") as file:
            file.write(
                COMMAND.format(name=name)
            )

        with open(com_path / "config.py", "w+") as file:
            file.write(
                CONFIG.format(name=name)
            )
        with open(com_path / "__init__.py", "w+") as file:
            file.write(f"from .main import {name}\n")

        with open(Path("src") / "__init__.py", "a+") as file:
            file.write(f"from .{name} import {name}\n")

        click.echo(
            click.style("Added a command ", fg="green") +\
            click.style(name, bold=True) +\
            click.style(" into path ", fg="green") +\
            click.style(str(Path("src") / f"{name}"), bold=True)
        )


@click.option(
    "-d", "--debug",
    is_flag=True,
    default=False,
    help="Debug mode (verbose output)"
)
@click.option(
    "--reload",
    is_flag=True,
    default=False,
    help="Reload a bot after files changing"
)
@click.option(
    "-o-t", "--once-time", "once_time",
    is_flag=True,
    default=False,
    help="Used for one times bot running. Bot is stoped after files changing"
)
@bot.command()
def run(reload, once_time, debug):
    """
    Run procces in bot
    """
    click.clear()
    if reload:
        args = sys.argv[1:]
        if "-r" in args:
            args.remove("-r")
        if "--reload" in args:
            args.remove("--reload")
        args.append("--once-time")

        # print("> All prints you see will be changed to logger later.")
        # prev_out = None
        # proc = subprocess.run(["bot", *args], stderr=subprocess.STDOUT)
        # prev_out = proc.stderr
        # while True:
        #     print("Run")
        #     proc = subprocess.run(["bot", *args], stderr=subprocess.STDOUT)
        #     if prev_out == proc.stderr and prev_out is not None:
        #         proc = subprocess.run(["bot", *args], capture_output=True)
        #     else:
        #         proc = subprocess.run(["bot", *args], stderr=subprocess.STDOUT)
        #
        #     prev_out = proc.stderr
        #     print("Reload...")
        print("> All prints you see will be changed to logger later.")
        while True:
            print("Run")
            proc = subprocess.run(["bot", *args])
            print("Reload...")

    elif once_time:
        # Your bot project path
        sys.path.append(os.getcwd())

        class AllEventsHandler(PatternMatchingEventHandler):
            def on_any_event(self, event):
                self.bot.reaload_now = True

        event_handler = AllEventsHandler(
            ignore_patterns=["__pycache__", "*.pyc"],
            ignore_directories=True
        )
        # Bot's
        import src
        config = attrdict.AttrMap(toml.load("config.toml"))

        settings = dict(
            token=config.api.token,
            group_id=config.api.group_id,
            version=config.api.version,
            delay=config.api.delay,
            wait=config.longpoll.wait,
            debug=debug
        )

        reactions = []
        signals = []
        for var in src.__dict__.values():
            if isinstance(var, vq.Reaction):
                reactions.append(var)
            elif isinstance(var, vq.Signal):
                signals.append(var)
        reactions = vq.ReactionsList(reactions)
        signals = vq.SignalsList(signals)

        bot = vq.Bot(reactions=reactions, signals=signals, **settings)

        AllEventsHandler.bot = bot

        observer = Observer()
        observer.schedule(event_handler, ".", recursive=True)
        observer.start()
        bot.run()
        observer.stop()
        observer.join()

    else:
        # Your bot project path
        sys.path.append(os.getcwd())

        # Bot's
        import src
        config = attrdict.AttrMap(toml.load("config.toml"))

        settings = dict(
            token=config.api.token,
            group_id=config.api.group_id,
            version=config.api.version,
            delay=config.api.delay,
            wait=config.longpoll.wait,
            debug=debug
        )

        reactions = []
        signals = []
        for var in src.__dict__.values():
            if isinstance(var, vq.Reaction):
                reactions.append(var)
            elif isinstance(var, vq.Signal):
                signals.append(var)
        reactions = vq.ReactionsList(reactions)
        signals = vq.SignalsList(signals)

        bot = vq.Bot(
            reactions=reactions,
            signals=signals,
            **settings
        )
        bot.run()


@click.option(
    "-o", "--on", "on",
    default=None,
    help="Signal name. By default it's the handler name"
)
@click.argument("name")
@bot.command()
def signal(name, on):
    """
    Add a signal in your bot
    """
    sig_name = on or name
    with open(Path("src") / f"{name}.py", "w+") as file:
        file.write(SIGNAL.format(name=sig_name))

    with open(Path("src") / "__init__.py", "a+") as file:
        file.write(f"from .{name} import {name}\n")

    click.echo(
        click.style("Added a hander on a signal ", fg="green") +\
        click.style(sig_name, bold=True) +\
        click.style(" into path ", fg="green") +\
        click.style(str(Path("src") / f"{name}.py"), bold=True)
    )

@bot.command()
def foo():
    click.echo(1)
    click.echo(2)
    click.clear()
    click.echo(3)

if __name__ == "__main__":
    bot()
