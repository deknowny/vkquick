from .base import Annotype
from vkquick.tools import User, UserAnno


class FwdUsers(Annotype, UserAnno):
    """
    User that sent a message
    """
    async def prepare(self, argname, event, func, bot, bin_stack):
        users = []
        for msg in event.object.message.frw_messages:
            user_id = msg.from_id
            user = await User(user_id=user_id).get_info(
                bot.api, **self.fields
            )
            users.append(user)

        return users
