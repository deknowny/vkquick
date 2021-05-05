from vkquick.bot import EventProcessingContext
from vkquick.ext.chatbot.bases.middleware import Middleware
from vkquick.ext.chatbot.providers.message import MessageProvider


class MakeMessageProviderOnNewMessage(Middleware):
    async def foreword(self, epctx: EventProcessingContext) -> None:
        if epctx.event.type == 4:
            updated_message = await epctx.bot.api.messages.get_by_id(
                ..., message_ids=epctx.event.content[1]
            )
            cultivated_message = updated_message["items"][0]
            epctx.extra["message_provider"] = MessageProvider.from_mapping(
                epctx.bot.api, cultivated_message
            )
        elif epctx.event.type in ("message_new", "message_reply"):
            if "message" in epctx.event.object:
                epctx.extra[
                    "message_provider"
                ] = MessageProvider.from_mapping(
                    epctx.bot.api, epctx.event.object["message"]
                )
            else:
                epctx.extra[
                    "message_provider"
                ] = MessageProvider.from_mapping(
                    epctx.bot.api, epctx.event.object
                )
        else:
            epctx.extra["message_provider"] = None
