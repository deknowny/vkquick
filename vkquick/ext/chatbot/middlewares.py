from vkquick.bases.middleware import Middleware
from vkquick.bot import EventProcessingContext
from vkquick.ext.chatbot.providers.message import MessageProvider


class MakeMessageProviderOnNewMessage(Middleware):
    async def foreword(self, epctx: EventProcessingContext) -> None:
        if epctx.event.type == 4:
            updated_message = epctx.bot.api.messages.get_by_id(
                ..., message_ids=epctx.event.content[1]
            )
            cultivated_message = updated_message["items"][0]
            epctx.extra["cultivated_message"] = MessageProvider.from_mapping(
                epctx.bot.api, cultivated_message
            )
        elif epctx.event.type == "message_new":
            if "message" in epctx.event.object:
                epctx.extra["cultivated_message"] = epctx.event.object[
                    "message"
                ]
            else:
                epctx.extra["cultivated_message"] = epctx.event.object
        else:
            epctx.extra["cultivated_message"] = None
