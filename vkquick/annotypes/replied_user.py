from .base import Annotype
from .user import User, UserAnno


class RepliedUser(Annotype, UserAnno):
    """
    User that sent a message
    """
    async def prepare(self, argname, event, func, bot, bin_stack):
        if "reply_message" in event.object.message:
            return await User(
                user_id=event.object.message.reply_message.from_id
            ).get_info(bot.api, *self.fields)
        else:
            return None
