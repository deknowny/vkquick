from typing import List

from .base import Annotype
from vkquick.tools import User, UserAnno


class FwdUsers(Annotype, UserAnno):
    """
    Список пользователей,
    находящиеся в пересланном сообщении
    (из параметра event.object.message.frw_messages).
    Если len(event.object.message.frw_messages) == 0,
    то передастся пустой список
    """

    async def prepare(self, argname, event, func, bin_stack) -> List[User]:
        users = []
        for msg in event.object.message.fwd_messages:
            user_id = msg.from_id
            user = await User(user_id=user_id).get_info(
                *self.fields, name_case=self.name_case
            )
            users.append(user)

        return users
