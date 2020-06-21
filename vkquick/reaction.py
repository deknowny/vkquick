import datetime as dt
from asyncio import create_task
from asyncio import iscoroutinefunction as icf
from inspect import signature, isgeneratorfunction

import click

from . import annotypes
from . import tools


class Reaction:
    """
    LongPoll's events handler
    """

    def __init__(
        self, *events_name,
    ):
        self.events_name = events_name if events_name else ...
        self.validators = []

    def __call__(self, code):
        self.code = code
        self.args = {}

        if hasattr(code, "validators"):
            PositionError = type("PositionError", (Exception,), {})
            raise PositionError("Reaction decorator should be the first")
            self.validators = code.validators

        self.command_args = {}
        self.payload_args = {}
        for name, value in signature(code).parameters.items():
            if (
                isinstance(value.annotation, type) and
                annotypes.CommandArgument in value.annotation.__bases__
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

    async def run(self, comkwargs):
        if icf(self.code):
            return await create_task(self.code(**comkwargs))
        else:
            return self.code(**comkwargs)

    @staticmethod
    def convert(conv):
        """
        Primitives to Annotypes
        """
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
    List with events handler
    """
    def has_event(self, event_name):
        for reaction in self:
            # Special don't react on ...
            if event_name in reaction.events_name:
                return True

        return False

    async def _send_message(self, api, event, message):
        """
        Send a meessage by user's returning in reaction
        """
        if isinstance(message, tools.Message):
            if message.params.peer_id is Ellipsis:
                message.params.peer_id = event.object.message.peer_id

            await api.messages.send(
                **message.params
            )
        elif message is None:
            return
        else:
            await api.messages.send(
                random_id=0,
                peer_id=event.object.message.peer_id,
                message=str(message)
            )

    @staticmethod
    def get_char(self):
        print("Show full event? (key)")
        return click.getchar()

    async def resolve(self, event, bot):
        header_printed = False

        for reaction in self:
            if event.type in reaction.events_name or reaction.events_name is Ellipsis:
                if not header_printed:
                    bot.debug_out(
                        click.style("[Reactions on ", bold=True) +\
                        click.style(event.type, fg="cyan") +\
                        "]" +\
                        click.style(
                            dt.datetime.now().strftime(" -- %Y-%m-%d %H:%M:%S"),
                            fg="bright_black"
                        )
                    )
                header_printed = True
                # Class for escaping race condition
                bin_stack = type("BinStack", (), {})
                bot.debug_out(click.style(reaction.code.__name__, fg="cyan"))
                for validator in reaction.validators:
                    if icf(validator.isvalid):
                        val = await validator.isvalid(
                            event, reaction, bot, bin_stack
                        )

                    else:
                        val = validator.isvalid(
                            event, reaction, bot, bin_stack
                        )

                    if not val[0]:
                        bot.debug_out(
                            f"-- {validator.__class__.__name__}: " +\
                            click.style(
                                "not valid", fg="red"
                            )
                        )
                        bot.debug_out(
                            "   -> " +\
                            click.style(
                                val[1], fg="red"
                            ), end="\n\n"
                        )
                        break
                    bot.debug_out(
                        f"-- {validator.__class__.__name__}: " +\
                        click.style(
                            "valid", fg="green"
                        )
                    )
                else:
                    comkwargs = {}
                    for name, value in reaction.args.items():
                        if icf(value.prepare):
                            content = await value.prepare(
                                argname=name,
                                event=event,
                                func=reaction,
                                bot=bot,
                                bin_stack=bin_stack
                            )
                        else:
                            content = value.prepare(
                                argname=name,
                                event=event,
                                func=reaction,
                                bot=bot,
                                bin_stack=bin_stack
                            )
                        comkwargs.update({name: content})


                    for key, value in comkwargs.items():
                        bot.debug_out(
                            "> " +\
                            click.style(key, fg="yellow") +\
                            f" = {value!r}"
                        )
                    print()
                    response = await reaction.run(comkwargs)

                    if isgeneratorfunction(reaction.code):
                        await self._send_message(
                            bot.api, event, "".join(response)
                        )
                    else:
                        await self._send_message(bot.api, event, response)
