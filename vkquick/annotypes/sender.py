from .base import Annotype
from vkquick.tools import User, UserAnno


__pdoc__ = {"Sender.prepare": Annotype.prepare.__doc__}


class Sender(Annotype, UserAnno):
    """
    Пользователь, отправивший сообщение
    """
    async def prepare(self, argname, event, func, bin_stack) -> User:
        return await User(
            user_id=event.object.message.from_id
        ).get_info(*self.fields)
