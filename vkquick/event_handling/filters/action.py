import enum

import vkquick.base.filter
import vkquick.events_generators.event


class ActionStatus(vkquick.base.filter.DecisionStatus):
    PASSED = enum.auto()
    NOT_PASSED = enum.auto()


class Action(vkquick.base.filter.Filter):

    passed_decision = vkquick.base.filter.Decision(True, "В сообщение содержатся нужное действие")
    not_passed_decision = vkquick.base.filter.Decision(False, "В сообщение не содержатся нужное действие")
    passed_response = vkquick.base.filter.FilterResponse(ActionStatus.PASSED, passed_decision)
    not_passed_response = vkquick.base.filter.FilterResponse(ActionStatus.NOT_PASSED, not_passed_decision)

    def __init__(self, *types):
        self.types = types

    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> vkquick.base.filter.FilterResponse:
        """
        Проверяет на действие в сообщение
        """
        message = event.get_message_object()
        if "action" in message and message.action.type in self.types:
            return self.passed_response
        return self.not_passed_response
