import enum

import vkquick.base.filter
import vkquick.events_generators.event


class RetractAccessForStatus(vkquick.base.filter.DecisionStatus):
    PASSED = enum.auto()
    NOT_PASSED = enum.auto()


class RetractAccessFor(vkquick.base.filter.Filter):
    """
    Ограничивает пользование командой определенным людям/сообществам
    """

    passed_decision = vkquick.base.filter.Decision(
        True, "Пользователь может пользоваться командой"
    )
    not_passed_decision = vkquick.base.filter.Decision(
        False, "Пользователь ине может пользоваться командой"
    )
    passed_response = vkquick.base.filter.FilterResponse(
        RetractAccessForStatus.PASSED, passed_decision
    )
    not_passed_response = vkquick.base.filter.FilterResponse(
        RetractAccessForStatus.NOT_PASSED, not_passed_decision
    )

    def __init__(self, *ids):
        self.ids = ids

    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> vkquick.base.filter.FilterResponse:
        if event.get_message_object().from_id not in self.ids:
            return self.passed_response
        return self.not_passed_response
