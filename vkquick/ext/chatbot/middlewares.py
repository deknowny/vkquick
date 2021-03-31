from vkquick.bases.middleware import Middleware
from vkquick.bot import EventProcessingContext


class ExtendUserLPNewMessage(Middleware):
    async def foreword(self, epctx: EventProcessingContext) -> None:
        if epctx.event.type == 4:
            updated_message = epctx.bot.api.messages.get_by_id(
                ..., message_ids=epctx.event.content[1]
            )
            epctx.extra["cultivated_message"] = updated_message["items"][0]
        elif epctx.event.type == "message_new":
            if "message" in epctx.event.object:
                epctx.extra["cultivated_message"] = epctx.event.object[
                    "message"
                ]
            else:
                epctx.extra["cultivated_message"] = epctx.event.object
        else:
            epctx.extra["cultivated_message"] = None


class MessageProviderInitializer(Middleware):
    async def foreword(self, epctx: EventProcessingContext) -> None:
        if epctx.event.type in ("message_new", 4):
            ...
