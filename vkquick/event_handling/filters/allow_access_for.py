import enum

import vkquick.base.filter
import vkquick.events_generators.event


class AllowAccessForStatus(vkquick.base.filter.DecisionStatus):
    PASSED = enum.auto()
    NOT_PASSED = enum.auto()


class AllowAccessFor(vkquick.base.filter.Filter):

    passed_decision = vkquick.base.filter.Decision(True, "Пользователь имеет доступ к команде")
    not_passed_decision = vkquick.base.filter.Decision(False, "Пользователь не имеет доступ к команде")
    passed_response = vkquick.base.filter.FilterResponse(AllowAccessForStatus.PASSED, passed_decision)
    not_passed_response = vkquick.base.filter.FilterResponse(AllowAccessForStatus.NOT_PASSED, not_passed_decision)

    def __init__(self, *ids):
        self.ids = ids

    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> vkquick.base.filter.FilterResponse:
        """
        Проверяет на доступ к команде
        """
        if event.get_message_object().from_id in self.ids:
            return self.passed_response
        return self.not_passed_response
