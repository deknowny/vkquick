from .base import Annotype
from .user import User


class Sender(Annotype):
    """
    User that sent a message
    """
    @staticmethod
    async def prepare(argname, event, func, bot, bin_stack):
        return await User(
            user_id=event.object.message.from_id
        ).get_info(bot.api)
