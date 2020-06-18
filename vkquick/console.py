import asyncio
import os
import sys
import datetime
import time
import pathlib
import importlib
import types
import subprocess

import click
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


CONFIG_PY = r"""
token = \"{token}\"
group_id = {group_id}
""".strip()


README = """
# {name}
VK Bot written on vkquick. Now is in developing.
""".strip()


COMMAND = r"""
import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES)
@vq.Reaction(\"message_new\")
def {name}():
    return config.ANSWER
""".strip()


CONFIG = r"""
NAMES = [\"{name}\"]
ANSWER = \"You used \`{name}\` command!\"
""".strip()



@click.group()
def bot(): ...


@click.option(
    "-o", "--owner",
    default="Anonymous",
    help="Bot owner. Will be added to a license file"
)
@click.option(
    "-t", "--token",
    default="Add token here",
    help="Token for group bot"
)
@click.option(
    "-gi", "--group-id", "group_id",
    default=0,
    type=int,
    help="Token's group ID"
)
@click.option(
    "-v", "--version",
    default=5.124,
    type=float,
    help="Token for group bot"
)
@click.argument("name")
@bot.command()
def new(
    owner, name, token,
    group_id, version
):
    """
    Create a new bot
    """
    year = datetime.datetime.now().year
    os.system(
        f"""
        mkdir -p {name}/src
        cd {name}
        touch LICENSE README.md config.py src/__init__.py
        echo "{MIT.format(
            owner=owner, year=year
        )}" >> LICENSE
        echo "{
            CONFIG_PY.format(
                token=token, version=version, group_id=group_id
        )}" >> config.py
        echo "{README.format(
            name=name.title()
        )}" >> README.md
        """
    )
    """
    Create folder to start easily writing bot
    """


@click.option(
    "-d", "--delete",
    is_flag=True,
    default=False
)
@click.argument("name")
@bot.command()
def com(name, delete):
    """
    Create a new command in the bot
    """
    if delete:
        os.system(
            f"""
            rm -r src/{name}
            """
        )
        with open("src/__init__.py", "r") as file:
                new_text = file.read().replace(
                    f"from .{name} import {name}\n", ""
                )
        with open("src/__init__.py", "w") as file:
            file.write(new_text)
    else:
        os.system(
            f"""
            mkdir -p src/{name}
            cd $_
            touch __init__.py config.py main.py
            echo "{COMMAND.format(
                name=name
            )}" >> main.py
            echo "{CONFIG.format(
                name=name
            )}" >> config.py
            echo "from .{name} import {name}" >> ../__init__.py
            echo "from .main import {name}" >> __init__.py
            """
        )


@click.option(
    "-r", "--reload",
    is_flag=True,
    default=False
)
@click.option(
    "-o-t", "--once-time", "once_time",
    is_flag=True,
    default=False
)
@bot.command()
def run(reload, once_time):
    """
    Run procces in bot
    """
    if reload:
        args = sys.argv[1:]
        if "-r" in args:
            args.remove("-r")
        if "--reload" in args:
            args.remove("--reload")
        args.append("--once-time")

        while True:
            subprocess.run(["bot", *args])

    elif once_time:
        # Your bot project path
        sys.path.append(os.getcwd())

        class AllEventsHandler(PatternMatchingEventHandler):
            def on_any_event(self, event):
                self.bot.reaload_now = True
        event_handler = AllEventsHandler(ignore_patterns=["__pycache__", "*.pyc"], ignore_directories=True)
        # Bot's
        import src
        import config

        settings = dict(
            token=config.token,
            group_id=config.group_id
        )
        if hasattr(config, "version"):
            settings.update(version=config.version)

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
        import config

        settings = dict(
            token=config.token,
            group_id=config.group_id
        )
        if hasattr(config, "version"):
            settings.update(version=config.version)

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

# Bin for my friend. No more
# from functools import wraps
#
#
# def prefix(*prefs):
#     def wrapper(func):
#         @wraps(func)
#         def inside(*args, **kwargs):
#             if


if __name__ == "__main__":
    bot()
