from __future__ import annotations

import dataclasses
import typing

from vkquick.chatbot.base.filter import BaseFilter
from vkquick.chatbot.exceptions import StopCurrentHandling
from vkquick.chatbot.utils import peer

if typing.TYPE_CHECKING:  # pragma: no cover
    from vkquick.chatbot.storages import NewMessage


class OnlyMe(BaseFilter):
    async def make_decision(self, ctx: NewMessage, **kwargs):
        if not ctx.msg.out:
            raise StopCurrentHandling()


class IgnoreBots(BaseFilter):
    async def make_decision(self, ctx: NewMessage, **kwargs):
        if ctx.msg.from_id < 0:
            raise StopCurrentHandling()

            
class IsReplyOrForward(vq.BaseFilter):
    async def make_decision(self, ctx: vq.NewMessage, **kwargs):
        if "fwd" not in ctx.event.content[7]:
            raise vq.StopCurrentHandling()
            

class ChatOnly(BaseFilter):
    async def make_decision(self, ctx: NewMessage, **kwargs):
        if ctx.msg.peer_id < peer():
            raise StopCurrentHandling()


class DirectOnly(BaseFilter):
    async def make_decision(self, ctx: NewMessage, **kwargs):
        if ctx.msg.peer_id >= peer():
            raise StopCurrentHandling()


@dataclasses.dataclass
class Dynamic(BaseFilter):
    executable: typing.Callable[[NewMessage], ...]

    async def make_decision(self, ctx: NewMessage, **kwargs):
        if not self.executable(ctx):
            raise StopCurrentHandling()
