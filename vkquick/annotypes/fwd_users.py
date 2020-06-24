from typing import List

from .base import Annotype
from vkquick.tools import User, UserAnno


__pdoc__ = {"FwdUsers.prepare": Annotype.prepare.__doc__}


class FwdUsers(Annotype, UserAnno):
    """
    Список пользователей,
    находящиеся в пересланном сообщении
    (из параметра event.object.message.frw_messages).
    Если len(event.object.message.frw_messages) == 0,
    то передастся пустой список
    """
    async def prepare(self, argname, event, func, bot, bin_stack) -> List[User]:
        users = []
        for msg in event.object.message.frw_messages:
            user_id = msg.from_id
            user = await User(user_id=user_id).get_info(
                bot.api, **self.fields
            )
            users.append(user)

        return users
