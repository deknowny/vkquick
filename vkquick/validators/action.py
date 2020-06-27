from .base import Validator
from vkquick.annotypes import Annotype


class Action(Validator, Annotype):
    """
    Декоратор для валидации сообщения
    на параметр `action` в ```event.object.message```
    (вход в беседу, выход из беседы...).

    Принимает `*types`-- Список обрабатываемых ```action.type```
    """

    def __init__(self, *types):
        self.types = types

    @staticmethod
    def prepare(argname, event, func, bin_stack):
        return event.object.message.action

    def isvalid(self, event, com, bin_stack):
        if (
            "action" in event.object.message and
            event.object.message.action.type in self.types
        ):
            return (True, "")
        return (False, "No action or action.type is an another")
