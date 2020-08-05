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

    def validate(self, event):
        if not (
            "action" in event.object.message
            and event.object.message.action.type in self.types
        ):
            raise ValueError("No action or action.type is an another")
