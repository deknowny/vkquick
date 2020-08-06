from typing import Union

from .base import Annotype
from vkquick.tools import User, UserAnno


class RepliedUser(Annotype, UserAnno):
    """
    Пользователь, находящийся в reply_message.
    Если такого нет -- возвращается None
    """

    async def prepare(
        self, argname, event, func, bin_stack
    ) -> Union[User, None]:
        if "reply_message" in event.object.message:
            return await User(
                user_id=event.object.message.reply_message.from_id
            ).get_info(*self.fields, name_case=self.name_case)
        else:
            return None
