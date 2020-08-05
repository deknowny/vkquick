from .base import Annotype
from vkquick.tools import User, UserAnno # , event_resolve as _
import vkquick as vq


class Sender(Annotype, UserAnno):
    """
    Пользователь, отправивший сообщение
    """

    async def prepare(self, argname, event, func, bin_stack) -> User:
        return await User(user_id=event.object.message.from_id).get_info(
            *self.fields, name_case=self.name_case
        )
