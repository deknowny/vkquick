from asyncio import create_task
from asyncio import iscoroutinefunction as icf
from inspect import signature, isgeneratorfunction


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

    async def resolve(self, event, bot):
        for reaction in self:

            if event.type in reaction.events_name or reaction.events_name is Ellipsis:
                # Class for escaping race condition
                bin_stack = type("BinStack", (), {})
                for validator in reaction.validators:
                    if icf(validator.isvalid):
                        val = await validator.isvalid(
                            event, reaction, bot, bin_stack
                        )
                    else:
                        val = validator.isvalid(
                            event, reaction, bot, bin_stack
                        )
                    if not val:
                        return

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

                response = await reaction.run(comkwargs)

                if isgeneratorfunction(reaction.code):

                    await self._send_message(
                        bot.api, event, "".join(response)
                    )
                else:
                    await self._send_message(bot.api, event, response)
