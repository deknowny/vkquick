"""
Реакции (обработчики LongPoll событий)
"""
import datetime as dt
from asyncio import create_task
from asyncio import iscoroutinefunction as icf
from inspect import signature
from inspect import isgeneratorfunction
from inspect import isasyncgenfunction
from typing import Union
from typing import Any

import click

from . import annotypes
from . import tools
from . import current


class Reaction:
    """
    Обработчик _корректного_ события LongPoll.ы
    """

    def __init__(
        self, *events_name,
    ):
        self.events_name = events_name if events_name else ...
        self.validators = []

    def __call__(self, code):
        self.code = code
        self.args = {}

        assert not hasattr(code, "validators"), "Invalid decorator position"

        self.command_args = {}
        self.payload_args = {}
        for name, value in signature(code).parameters.items():
            if (
                isinstance(value.annotation, type)
                and annotypes.CommandArgument in value.annotation.__bases__
            ):
                raise ValueError(
                    "Annotype should be the instance, got "
                    f"{value.annotation}\n"
                    f"For example: "
                    f"vq.{value.annotation.__name__}() instead "
                    f"vq.{value.annotation.__name__}"
                )
            if (
                isinstance(value.annotation, annotypes.CommandArgument)
                or value.annotation is int
                or value.annotation is str
                or isinstance(value.annotation, list)
            ):
                self.command_args.update(
                    {name: Reaction.convert(value.annotation)}
                )

            else:
                conv = Reaction.convert(value.annotation)

                self.payload_args.update({name: conv})

            self.args.update({name: Reaction.convert(value.annotation)})

        return self

    async def run(self, comkwargs: dict) -> Union[str, Any, "vkquck.Message"]:
        """
        Запускает код реакции с переданными comkwargs
        """
        if icf(self.code):
            return await self.code(**comkwargs)
        else:
            return self.code(**comkwargs)

    @staticmethod
    def convert(conv):
        """
        Конвертирует "примитивы" в Annotypes
        """
        # NOTE: int and str работают
        # только как одиночные типы, либо
        # внутри [], т.е. `vq.Optional(int)`
        # -- невалидно
        if conv is int:
            return annotypes.Integer()
        elif conv is str:
            return annotypes.String()
        elif isinstance(conv, list):
            return annotypes.List(Reaction.convert(conv[0]))
        else:
            return conv


class ReactionsList(list):
    """
    Список с обработчиками корректных событий
    """

    def has_event(self, event_name):
        for reaction in self:
            # Special don't react on ...
            if event_name in reaction.events_name:
                return True

        return False

    @staticmethod
    async def _send_message(event, message):
        """
        Send a meessage by user's returning in reaction
        """
        if isinstance(message, tools.Message):
            if message.params.peer_id is Ellipsis:
                message.params.peer_id = event.object.message.peer_id

            await current.api.messages.send(**message.params)
        elif message is None:
            # Если реакция ничего не вернула
            return
        else:
            await current.api.messages.send(
                random_id=0,
                peer_id=event.object.message.peer_id,
                message=str(message),
            )

    async def validate(
        self,
        event: "vkquick.Event",
        reaction: "vkquick.Reaction",
        bin_stack: type,
    ):
        """
        Валидирует конкретную команду
        """
        # Текстовый блок про реакциию в дебаггере
        TEXT = click.style(reaction.code.__name__, fg="cyan") + "\n"

        for validator in reaction.validators:
            if icf(validator.isvalid):
                val = await validator.isvalid(event, reaction, bin_stack)

            else:
                val = validator.isvalid(event, reaction, bin_stack)

            if not val[0]:
                TEXT += f"-- {validator.__class__.__name__}: " + click.style(
                    "not valid\n", fg="red"
                )

                TEXT += "   -> " + click.style(val[1] + "\n", fg="red")

                current.bot.debug_out(TEXT)
                break

            TEXT += f"-- {validator.__class__.__name__}: " + click.style(
                "valid\n", fg="green"
            )

        else:
            comkwargs = {}
            for name, value in reaction.args.items():
                if icf(value.prepare):
                    content = await value.prepare(
                        argname=name,
                        event=event,
                        func=reaction,
                        bin_stack=bin_stack,
                    )
                else:
                    content = value.prepare(
                        argname=name,
                        event=event,
                        func=reaction,
                        bin_stack=bin_stack,
                    )
                comkwargs.update({name: content})

            for key, value in comkwargs.items():
                TEXT += (
                    "> " + click.style(key, fg="yellow") + f" = {value!r}\n"
                )
            current.bot.debug_out(TEXT)
            response = await reaction.run(comkwargs)

            if isgeneratorfunction(reaction.code):
                await self._send_message(event, "".join(response))
            elif isasyncgenfunction(reaction.code):
                await self._send_message(
                    event, "".join([mes async for mes in response])
                )
            else:
                await self._send_message(event, response)

    async def resolve(self, event: "vkquick.Event"):
        # Был ли выведен хедер в режиме дебага
        header_printed = False

        for reaction in self:

            if (
                event.type in reaction.events_name
                or reaction.events_name is Ellipsis
            ):
                if not header_printed:
                    if current.bot.debug:
                        click.clear()
                    current.bot.debug_out(
                        click.style("[Reactions on ", bold=True)
                        + click.style(event.type, fg="cyan")
                        + click.style("]", bold=True)
                        + click.style(
                            dt.datetime.now().strftime(
                                " -- %Y-%m-%d %H:%M:%S"
                            ),
                            fg="bright_black",
                        )
                    )

                header_printed = True
                # Класс для избежания гонки данных
                bin_stack = type("BinStack", (), {})
                create_task(self.validate(event, reaction, bin_stack))
