import typing as ty

from vkquick.bot import EventProcessingContext, Bot
from vkquick.api import API
from vkquick.exceptions import ExpectedMiddlewareToBeUsed
from vkquick.ext.chatbot.lite_api import LiteAPI
from vkquick.ext.chatbot.wrappers.message import Message
from vkquick.ext.chatbot.wrappers.page_entities import PageEntity, User, Group


class MessageProvider:
    def __init__(self, epctx: EventProcessingContext) -> None:
        try:
            self._msg: Message = Message(self._epctx.extra["cultivated_message"])
        except KeyError as err:
            raise ExpectedMiddlewareToBeUsed("ExtendUserLPNewMessage") from err
        self._lite_api: LiteAPI = LiteAPI(epctx.bot.api)
        self._epctx: EventProcessingContext = epctx

    @property
    def epctx(self) -> EventProcessingContext:
        return self._epctx

    @property
    def api(self) -> API:
        return self._epctx.bot.api

    @property
    def lite_api(self) -> LiteAPI:
        return self._lite_api

    @property
    def bot(self) -> Bot:
        return self._epctx.bot

    @property
    def msg(self) -> Message:
        return self._msg

    async def fetch_any_sender(self) -> PageEntity:
        if self._msg.from_id > 0:
            return await self._lite_api.fetch_user(self._msg.from_id)
        else:
            return await self._lite_api.fetch_group(self._msg.from_id)

    async def fetch_user_sender(self) -> User:
        if self._msg.from_id < 0:
            raise TypeError("Message was sent by a group. Can't fetch user")
        else:
            return await self._lite_api.fetch_user(self._msg.from_id)

    async def fetch_group_sender(self) -> Group:
        if self._msg.from_id > 0:
            raise TypeError("Message was sent by a user. Can't fetch group")
        else:
            return await self._lite_api.fetch_group(self._msg.from_id)
