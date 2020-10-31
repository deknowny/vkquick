import typing as ty

import vkquick.base.filter
import vkquick.events_generators.event


class Action(vkquick.base.filter.Filter):

    passed_decision = "В сообщение содержатся нужное действие"
    not_passed_decision = "В сообщение не содержатся нужное действие"

    def __init__(self, *types):
        self.types = types

    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Tuple[bool, str]:
        """
        Проверяет на действие в сообщение
        """
        message = event.get_message_object()
        if "action" in message and message.action.type in self.types:
            return True, self.passed_decision
        return False, self.not_passed_decision
