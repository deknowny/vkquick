from vkquick.event_handler.context import EventHandlingContext
from vkquick.exceptions import ExpectedMiddlewareToBeUsed
from vkquick.ext.chatbot.providers.message import MessageProvider


class CommandContext(EventHandlingContext):
    def __post_init__(self):
        try:
            self.epctx.extra["cultivated_message"]
        except KeyError as err:
            raise ExpectedMiddlewareToBeUsed(
                "MakeMessageProviderOnNewMessage"
            ) from err

    @property
    def mp(self) -> MessageProvider:
        return self.epctx.extra["message_provider"]
