from .base import Validator


class Action(Validator):
    """
    Декоратор для валидации сообщения
    на параметр `action` в ```event.object.message```
    (вход в беседу, выход из беседы...).

    Принимает `*types`-- Список обрабатываемых ```action.type```
    """

    def __init__(self, *types):
        self.types = types

    def isvalid(self, event, com, bin_stack):
        if (
            "action" in event.object.message
            and event.object.message.action.type in self.types
        ):
            return (True, "")
        return (False, "No action or action.type is an another")
